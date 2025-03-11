from sqlmodel import Field, SQLModel
from typing import List, Optional
from datetime import datetime
from app.schemas.workspace import WorkspaceStatus

# Workspace Member
class WorkspaceMember(SQLModel, table=True):
  __tablename__ = "workspacemembers"

  id: int = Field(primary_key=True)
  workspace_id: int = Field(foreign_key="workspaces.id")
  member_id: int = Field(foreign_key="users.id")  
  role: str = Field(default="User")
  created_at: datetime = Field(default_factory=datetime.utcnow)

# Workspace
class Workspace(SQLModel, table=True):
  __tablename__ = "workspaces"

  id: int = Field(default=None, primary_key=True)
  name: str
  description: Optional[str] = None
  status:WorkspaceStatus = Field(default=WorkspaceStatus.active)
  owner_id: int = Field(default=None, foreign_key="users.id")  
  created_at: datetime = Field(default_factory=datetime.utcnow)