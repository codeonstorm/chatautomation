from uuid import UUID
import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, delete

from app.core.auth import get_current_user
from app.core.database import get_session

from app.models.intents import Intent, Action, Parameter
from app.schemas.newIntent import NewIntentRead, NewIntentCreate, NewIntentUpdate, ActionBase, ParameterBase
from app.schemas.response import ResponseSchema
from app.schemas.user import UserRead

router = APIRouter(prefix="/{service_id}/{chatbot_uuid}/intents", tags=["intents"])

@router.post("", response_model=NewIntentRead)
def create_intent(
    service_id: int,
    chatbot_uuid: UUID,
    intent_in: NewIntentCreate,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    action_data = intent_in.action
    parameters_data = action_data.parameters

    # Create the Intent object
    intent = Intent(
        **intent_in.model_dump(exclude={"action"}),
        service_id=service_id,
        chatbot_uuid=chatbot_uuid
    )
    db.add(intent)
    db.flush() 
    
    # Create the Action object
    action = Action(
        intent_id=intent.id,
        name=action_data.name,
        webhook=action_data.webhook
    )
    db.add(action)
    db.flush()

    # Create Parameter objects
    parameters = [
        Parameter(
            action_id=action.id,
            parameter=param.parameter,
            required=param.required,
            message=param.message
        )
        for param in parameters_data
    ]
    db.add_all(parameters)

    # Commit all at once
    db.commit()

    response = NewIntentRead(
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
                    message=p.message
                ) for p in parameters
            ]
        )
    )

    return response

@router.get("/{intent_id}", response_model=NewIntentRead)
def read_intent(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
    parameters = db.exec(select(Parameter).where(Parameter.action_id == action.id)).all()

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
                    parameter=param.parameter,
                    required=param.required,
                    message=param.message
                ) for param in parameters
            ]
        )
    )

@router.get("", response_model=list[NewIntentRead])
def get_all_intents(
    service_id: int,
    chatbot_uuid: UUID,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    intents = db.exec(
        select(Intent).where(
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid
        )
    ).all()

    results = []
    for intent in intents:
        action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
        parameters = db.exec(select(Parameter).where(Parameter.action_id == action.id)).all()
        results.append(NewIntentRead(
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
                        parameter=param.parameter,
                        required=param.required,
                        message=param.message
                    ) for param in parameters
                ]
            )
        ))
    return results

@router.patch("/{intent_id}", response_model=NewIntentRead)
def update_intent(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    intent_update: NewIntentUpdate,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    # Update intent fields
    for key, value in intent_update.model_dump(exclude={"action"}).items():
        setattr(intent, key, value)

    # Update action
    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()
    action_data = intent_update.action
    action.name = action_data.name
    action.webhook = action_data.webhook

    # Delete old parameters and add new ones
    db.exec(delete(Parameter).where(Parameter.action_id == action.id))
    db.flush()

    new_parameters = [
        Parameter(
            action_id=action.id,
            parameter=param.parameter,
            required=param.required,
            message=param.message
        )
        for param in action_data.parameters
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
                    parameter=p.parameter,
                    required=p.required,
                    message=p.message
                ) for p in new_parameters
            ]
        )
    )

@router.delete("/{intent_id}", response_model=ResponseSchema)
def delete_intent(
    service_id: int,
    chatbot_uuid: UUID,
    intent_id: int,
    db: Session = Depends(get_session),
    current_user: UserRead = Depends(get_current_user),
):
    intent = db.exec(
        select(Intent).where(
            Intent.id == intent_id,
            Intent.service_id == service_id,
            Intent.chatbot_uuid == chatbot_uuid
        )
    ).first()
    if not intent:
        raise HTTPException(status_code=404, detail="Intent not found")

    # Check for action
    action = db.exec(select(Action).where(Action.intent_id == intent.id)).first()

    if action:
        # Delete related parameters
        parameters = db.exec(select(Parameter).where(Parameter.action_id == action.id)).all()
        for param in parameters:
            db.delete(param)
        db.delete(action)

    db.delete(intent)
    db.commit()

    return ResponseSchema(success=True, message="Intent deleted successfully")
