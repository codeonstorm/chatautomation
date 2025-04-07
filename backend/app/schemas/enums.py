from enum import Enum

# class ServicePlanType(str, Enum):
#   free = "free"
#   silver = "silver"
#   gold = "gold"
#   premium = "premium"

# class BaseStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"

# class ServiceStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"

# class UserStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"

# class ChatbotStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"

# class DomainStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"

# class WorkspaceStatus(str, Enum):
#   active = "active"
#   inactive = "inactive"
#   archived = "archived"


# Enums
class StatusEnum(str, Enum):
    enabled = "enabled"
    disabled = "disabled"
    deleted = "deleted"


class UserRoleEnum(str, Enum):
    superadmin = "superadmin"
    admin = "admin"
    user = "user"


class VerifiedEnum(str, Enum):
    true = "true"
    false = "false"


class FeedbackEnum(str, Enum):
    positive = "positive"
    neutral = "neutral"
    negative = "negative"


class ChatbotTypeEnum(str, Enum):
    sales = "sales"
    support = "support"
    onboarding = "onboarding"
    feedback = "feedback"
    booking = "booking"
    ecommerce = "e-commerce"
    internal_assistant = "internal_assistant"
    knowledge_base = "knowledge_base"
    marketing = "marketing"
    event = "event"
    education = "education"
    healthcare = "healthcare"
    entertainment = "entertainment"
    news = "news"
    custom = "custom"
