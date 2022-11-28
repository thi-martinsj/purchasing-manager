from flask_restx import Model, fields

health = Model(
    name="health", service=fields.String(example="Purchasing Manager"), version=fields.String(example="1.0.0")
)


client = Model(
    name="client",
    id=fields.String(
        description="Client unique identifier", required=False, example="677db4c7-3f29-4393-af2a-73f29cf115d5"
    ),
    created_dt=fields.DateTime(
        description="Client creation date", required=False, example="2022-11-27 14:01:47.585 -0300"
    ),
    updated_dt=fields.DateTime(
        description="The date the client was updated", required=False, example="2022-11-27 14:01:47.585 -0300"
    ),
    full_name=fields.String(description="Client full name", required=True, example="Fulano Beltrano da Silva"),
    document=fields.String(description="Client document number (CPF)", required=True, example="12345678900"),
    phone=fields.String(description="Client phone number", required=True, example="11999998888"),
    email=fields.String(description="Client email", required=True, example="fulanodasilva@example.com"),
)


internal_server_error = Model(
    name="internal_server_error",
    message=fields.String(description="Error message", required=False, example="Internal Server Error"),
)


not_found_error = Model(
    name="not_found_error",
    message=fields.String(description="Error message", required=False, example="Resource not found"),
)


invalid_payload = Model(
    name="invalid_payload",
    message=fields.String(
        description="Invalid payload", required=False, example="Missing the following attribute: 'name'"
    ),
)
