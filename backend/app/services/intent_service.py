from uuid import UUID
from fastapi import HTTPException
from sqlmodel import Session, select, delete

from app.models.intents import Intent, Action, Parameter
from app.schemas.newIntent import (
    NewIntentCreate,
    NewIntentUpdate,
    NewIntentRead,
    ActionBase,
    ParameterBase,
)


def create_intent(
    service_id: int, chatbot_uuid: UUID, intent_in: NewIntentCreate, db: Session
) -> NewIntentRead:
    action_data = intent_in.action
    parameters_data = action_data.parameters

    intent = Intent(
        **intent_in.model_dump(exclude={"action"}),
        service_id=service_id,
        chatbot_uuid=chatbot_uuid
    )
    db.add(intent)
    db.flush()

    action = Action(
        intent_id=intent.id, name=action_data.name, webhook=action_data.webhook
    )
    db.add(action)
    db.flush()

    parameters = [
        Parameter(
            action_id=action.id,
            parameter=p.parameter,
            required=p.required,
            message=p.message,
        )
        for p in parameters_data
    ]
    db.add_all(parameters)
    db.commit()

    return NewIntentRead(
        id=intent.id,
        name=intent.name,
        description=intent.description,
        phrases=intent.phrases,
        default_intent_responses=intent.default_intent_responses,
        service_id=intent.service_id,
        chatbot_uuid=intent.chatbot_uuid,
        created_at=intent.created_at,
        updated_at=intent.updated_at,
        action=ActionBase(
            name=action.name,
            webhook=action.webhook,
            parameters=[
                ParameterBase(
                    parameter=p.parameter, required=p.required, message=p.message
                )
                for p in parameters
            ],
        ),
    )


def get_intent(
    service_id: int, chatbot_uuid: UUID, intent_id: int, db: Session
) -> NewIntentRead:
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid,
        )
    ).first()

    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
    parameters = db.exec(
        select(Parameter).where(Parameter.action_id == action.id)
    ).all()

    return NewIntentRead(
        id=intent.id,
        name=intent.name,
        description=intent.description,
        phrases=intent.phrases,
        default_intent_responses=intent.default_intent_responses,
        service_id=intent.service_id,
        chatbot_uuid=intent.chatbot_uuid,
        created_at=intent.created_at,
        updated_at=intent.updated_at,
        action=ActionBase(
            name=action.name,
            webhook=action.webhook,
            parameters=[
                ParameterBase(
                    parameter=p.parameter, required=p.required, message=p.message
                )
                for p in parameters
            ],
        ),
    )


def get_all_intents(
    chatbot_uuid: UUID, db: Session
) -> list[NewIntentRead]:
    intents = db.exec(
        select(Intent).where(
            # Intent.service_id == service_id, 
            Intent.chatbot_uuid == chatbot_uuid
        )
    ).all()

    results = []
    for intent in intents:
        action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
        parameters = db.exec(
            select(Parameter).where(Parameter.action_id == action.id)
        ).all()
        results.append(
            NewIntentRead(
                id=intent.id,
                name=intent.name,
                description=intent.description,
                phrases=intent.phrases,
                default_intent_responses=intent.default_intent_responses,
                service_id=intent.service_id,
                chatbot_uuid=intent.chatbot_uuid,
                created_at=intent.created_at,
                updated_at=intent.updated_at,
                action=ActionBase(
                    name=action.name,
                    webhook=action.webhook,
                    parameters=[
                        ParameterBase(
                            parameter=p.parameter,
                            required=p.required,
                            message=p.message,
                        )
                        for p in parameters
                    ],
                ),
            )
        )
    return results


def update_intent(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    intent_update: NewIntentUpdate,
    db: Session,
) -> NewIntentRead:
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid,
        )
    ).first()

    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    for key, value in intent_update.model_dump(exclude={"action"}).items():
        setattr(intent, key, value)

    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
    action_data = intent_update.action
    action.name = action_data.name
    action.webhook = action_data.webhook

    db.exec(delete(Parameter).where(Parameter.action_id == action.id))
    db.flush()

    new_parameters = [
        Parameter(
            action_id=action.id,
            parameter=p.parameter,
            required=p.required,
            message=p.message,
        )
        for p in action_data.parameters
    ]
    db.add_all(new_parameters)

    db.commit()
    db.refresh(intent)

    return NewIntentRead(
        id=intent.id,
        name=intent.name,
        description=intent.description,
        phrases=intent.phrases,
        default_intent_responses=intent.default_intent_responses,
        service_id=intent.service_id,
        chatbot_uuid=intent.chatbot_uuid,
        created_at=intent.created_at,
        updated_at=intent.updated_at,
        action=ActionBase(
            name=action.name,
            webhook=action.webhook,
            parameters=[
                ParameterBase(
                    parameter=p.parameter, required=p.required, message=p.message
                )
                for p in new_parameters
            ],
        ),
    )


def delete_intent(service_id: int, chatbot_uuid: UUID, intent_id: int, db: Session):
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid,
        )
    ).first()

    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
    if action:
        parameters = db.exec(
            select(Parameter).where(Parameter.action_id == action.id)
        ).all()
        for param in parameters:
            db.delete(param)
        db.delete(action)

    db.delete(intent)
    db.commit()

    return {"success": True, "message": "Intent deleted successfully"}
