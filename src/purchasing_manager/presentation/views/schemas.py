from flask_restx import Model, fields

health = Model(
    name="health", service=fields.String(example="Purchasing Manager"), version=fields.String(example="1.0.0")
)
