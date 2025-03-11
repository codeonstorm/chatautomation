from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.auth import get_current_active_user
from app.core.database import get_session
from app.models.workspace import Workspace, WorkspaceMember
from app.schemas.workspace import (
  WorkspaceStatus,
  WorkspaceCreate,
  WorkspaceRead,
  WorkspaceUpdate,
  WorkspaceMemberCreate,
  WorkspaceMemberUpdate,
  WorkspaceMemberRead,
)

router = APIRouter()

@router.post("", response_model=WorkspaceRead)
def create_workspace(
  workspace_in: WorkspaceCreate,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  db_workspace = Workspace(
    **workspace_in.model_dump(),
    status=WorkspaceStatus.active,
    owner_id=current_user.id
  )
  session.add(db_workspace)
  session.commit()
  session.refresh(db_workspace)

  # Add the owner as a member
  member = WorkspaceMember(
    workspace_id=db_workspace.id,
    member_id=current_user.id,
    role="Owner"
  )
  session.add(member)
  session.commit()
  session.refresh(member)

  # Return the workspace with role and members
  result = WorkspaceRead(
    # **db_workspace.model_dump(),
    id = db_workspace.id,
    name = db_workspace.name,
    description = db_workspace.description,
    owner_id = db_workspace.owner_id,
    status = db_workspace.status,
    created_at = db_workspace.created_at,
    members = [WorkspaceMemberRead(
      workspace_id = member.workspace_id,
      member_id = member.member_id,
      role = member.role,
      created_at = member.created_at
    )]
  )
  return result

@router.get("", response_model=List[WorkspaceRead])
async def get_workspaces(
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Get all workspaces where the user is a member
  members = session.exec(
    select(WorkspaceMember).where(WorkspaceMember.member_id == current_user.id)
  ).all()

  workspace_ids = [member.workspace_id for member in members]

  if not workspace_ids:
    return []

  workspaces = session.exec(
    select(Workspace).where(Workspace.id.in_(workspace_ids))
  ).all()


  # For each workspace, get its members
  result = []
  for workspace in workspaces:
    workspace_members = session.exec(
      select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace.id)
    ).all()

    result.append(
      WorkspaceRead(
        **workspace.model_dump(),
        members=[WorkspaceMemberRead(**member.model_dump()) for member in workspace_members]
      )
    )

  return result

@router.get("/{workspace_id}", response_model=WorkspaceRead)
async def get_workspace(
  workspace_id: str,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")
  
  # Check if user is a member
  member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.member_id == current_user.id
    )
  ).first()
  
  if not member:
    raise HTTPException(status_code=403, detail="You don't have access to this workspace")
  
  # Get all members of the workspace
  workspace_members = session.exec(
    select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
  ).all()
  
  return WorkspaceRead(
    **workspace.dict(),
    role=member.role,
    members=[WorkspaceMemberRead(**m.dict()) for m in workspace_members]
  )

@router.patch("/{workspace_id}", response_model=WorkspaceRead)
async def update_workspace(
  workspace_id: str,
  workspace_update: WorkspaceUpdate,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user)
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")
  
  # Check if user is an admin or owner
  member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.member_id == current_user.id
    )
  ).first()
  
  if not member or member.role not in ["Owner", "Admin"]:
    raise HTTPException(status_code=403, detail="You don't have permission to update this workspace")
  
  # Update workspace
  for key, value in workspace_update.dict(exclude_unset=True).items():
    setattr(workspace, key, value)
  
  session.add(workspace)
  session.commit()
  session.refresh(workspace)
  
  # Get all members of the workspace
  workspace_members = session.exec(
    select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
  ).all()
  
  return WorkspaceRead(
    **workspace.model_dump(),
    role=member.role,
    members=[WorkspaceMemberRead(**m.model_dump()) for m in workspace_members]
  )

@router.delete("/{workspace_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workspace(
  workspace_id: str,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")

  # Check if user is the owner
  member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.member_id == current_user.id
    )
  ).first()

  if not member or member.role != "Owner":
    raise HTTPException(status_code=403, detail="Only the workspace owner can delete it")

  # Delete all members first
  members = session.exec(
    select(WorkspaceMember).where(WorkspaceMember.workspace_id == workspace_id)
  ).all()

  for member in members:
    session.delete(member)

  # Delete workspace
  session.delete(workspace)
  session.commit()

  return None

@router.post("/{workspace_id}/members", response_model=WorkspaceMemberRead)
async def add_workspace_member(
  workspace_id: str,
  member: WorkspaceMemberCreate,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")

  # Check if user is an admin or owner
  current_member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.user_id == current_user.id
    )
  ).first()

  if not current_member or current_member.role not in ["Owner", "Admin"]:
    raise HTTPException(status_code=403, detail="You don't have permission to add members")

  # Check if the role is valid
  if member.role not in ["Admin", "User"]:
    raise HTTPException(status_code=400, detail="Invalid role. Must be 'Admin' or 'User'")

  # Check if user is already a member
  existing_member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.email == member.email
    )
  ).first()

  if existing_member:
    raise HTTPException(status_code=400, detail="User is already a member of this workspace")

  # In a real app, you would check if the user exists and get their details
  # For this example, we'll just use the email as the name
  user_name = member.email.split("@")[0]
  user_id = f"user-{uuid.uuid4()}"  # Generate a mock user ID

  # Create new member
  db_member = WorkspaceMember(
    workspace_id=workspace_id,
    user_id=user_id,
    email=member.email,
    name=user_name,
    role=member.role
  )

  session.add(db_member)
  session.commit()
  session.refresh(db_member)

  return WorkspaceMemberRead(**db_member.dict())

@router.patch("/{workspace_id}/members/{member_id}", response_model=WorkspaceMemberRead)
async def update_workspace_member(
  workspace_id: str,
  member_id: str,
  member_update: WorkspaceMemberUpdate,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")

  # Check if user is an admin or owner
  current_member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.user_id == current_user.id
    )
  ).first()

  if not current_member or current_member.role not in ["Owner", "Admin"]:
    raise HTTPException(status_code=403, detail="You don't have permission to update members")

  # Check if the member exists
  member = session.get(WorkspaceMember, member_id)
  if not member or member.workspace_id != workspace_id:
    raise HTTPException(status_code=404, detail="Member not found in this workspace")

  # Check if the role is valid
  if member_update.role and member_update.role not in ["Owner", "Admin", "User"]:
    raise HTTPException(status_code=400, detail="Invalid role. Must be 'Owner', 'Admin', or 'User'")

  # Special handling for Owner role
  if member_update.role == "Owner":
    # Only current owner can transfer ownership
    if current_member.role != "Owner":
      raise HTTPException(status_code=403, detail="Only the workspace owner can transfer ownership")

    # Update current owner to Admin
    current_member.role = "Admin"
    session.add(current_member)

  # Update member
  for key, value in member_update.dict(exclude_unset=True).items():
    setattr(member, key, value)

  session.add(member)
  session.commit()
  session.refresh(member)

  return WorkspaceMemberRead(**member.dict())

@router.delete("/{workspace_id}/members/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_workspace_member(
  workspace_id: str,
  member_id: str,
  session: Session = Depends(get_session),
  current_user: dict = Depends(get_current_active_user),
):
  # Check if workspace exists
  workspace = session.get(Workspace, workspace_id)
  if not workspace:
    raise HTTPException(status_code=404, detail="Workspace not found")

  # Check if user is an admin or owner
  current_member = session.exec(
    select(WorkspaceMember).where(
      WorkspaceMember.workspace_id == workspace_id,
      WorkspaceMember.user_id == current_user.id
    )
  ).first()

  if not current_member or current_member.role not in ["Owner", "Admin"]:
    raise HTTPException(status_code=403, detail="You don't have permission to remove members")

  # Check if the member exists
  member = session.get(WorkspaceMember, member_id)
  if not member or member.workspace_id != workspace_id:
    raise HTTPException(status_code=404, detail="Member not found in this workspace")

  # Cannot remove the owner
  if member.role == "Owner":
    raise HTTPException(status_code=403, detail="Cannot remove the workspace owner")

  # Delete the member
  session.delete(member)
  session.commit()

  return None
