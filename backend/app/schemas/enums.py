from enum import Enum

class ServicePlanType(str, Enum):
  SERVICE1 = "free"
  SERVICE2 = "silver"
  SERVICE3 = "gold"
  SERVICE4 = "premium"

class BaseStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"

class ServiceStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"

class UserStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"

class ChatbotStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"

class DomainStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"

class WorkspaceStatus(str, Enum):
  ACTIVE = "active"
  INACTIVE = "inactive"
  ARCHIVED = "archived"
