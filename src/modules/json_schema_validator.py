import jsonschema
import json
from functools import wraps
from jsonschema.exceptions import ValidationError
from flask import Flask, current_app as app, request


class cls_json_schema_validator:
    """
    A class to handle JSON schema validation.
    """

    @staticmethod
    def validate_json(schema):

        """
        Decorator to validate JSON data against a provided JSON schema.

        :param schema: The JSON schema to validate against.
        :return: Decorator function.
        """

        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):

                validation_schema = json.load(open(app.config['API_JSON_SCHEMA']))

                schema_def = validation_schema['schema'].get(schema)
                app.logger.debug(f"JSON schema validation done for --->> {schema_def} ")
                # Assume JSON data is passed as the first argument or in `json_data` keyword argument
                global json_data
                if request.method == 'POST':
                    json_data = request.json
                    app.logger.debug(json_data)
                elif request.method == 'GET':
                    json_data = json.loads(json.dumps(dict(request.args)))
                    if json_data is None or not json_data:
                        json_data = request.json

                if json_data is None:
                    raise ValueError("No JSON data provided for validation")

                # Validate the JSON data using the provided schema
                try:
                    jsonschema.validate(instance=json_data, schema=schema_def,
                                        format_checker=jsonschema.FormatChecker())
                    app.logger.debug(f"JSON schema validation done for --->> {schema} ")
                except ValidationError as e:

                    # Extract the relevant part of the error path
                    path = e.path[-1] if e.path else 'unknown'  # For Key error occurred
                    error_type = e.validator  # for which proper error occurred
                    if path == 'unknown':
                        msg = format(e.message)
                    else:
                        msg = schema_def['properties'][path]['errorMessage'][error_type]
                    return {
                        "error": f"Request validation error: {msg}",
                        "status": "failure"}, 400

                # If validation passes, call the original function
                return func(*args, **kwargs)

            return wrapper

        return decorator
