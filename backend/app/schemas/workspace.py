from typing import Optional, List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from enum import Enum

class WorkspaceStatus(str, Enum):
  active = "active"
  inactive = "inactive"
  archived = "archived"

#  WorkspaceMember
class WorkspaceMemberBase(BaseModel):
  workspace_id: int
  member_id: int
  role: str 

class WorkspaceMemberCreate(WorkspaceMemberBase):
  pass

class WorkspaceMemberRead(WorkspaceMemberBase):
  # id: int
  created_at: datetime

class WorkspaceMemberUpdate(BaseModel):
  role: Optional[str] = None


# Workspace
class WorkspaceBase(BaseModel):
  id: int
  name: str
  description: Optional[str] = None
  owner_id: int
  status: WorkspaceStatus
  created_at: datetime

class WorkspaceCreate(BaseModel):
  name: str
  description: Optional[str] = None

class WorkspaceUpdate(BaseModel):
  name: str
  description: Optional[str] = None
  status: WorkspaceStatus

class WorkspaceRead(WorkspaceBase):
  members: List[WorkspaceMemberRead]
