import logging
import pytest
import traceback
from pytest_bdd import scenario, given, when, then, parsers
from hamcrest import assert_that, equal_to

from step_helpers import file_handler
from uk_bin_collection.uk_bin_collection import collect_data

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

@scenario("../features/validate_council_outputs.feature", "Validate Council Output")
def test_scenario_outline():
    pass


@pytest.fixture
def context():
    class Context(object):
        pass

    return Context()


@given(parsers.parse("the council: {council_name}"))
def get_council_step(context, council_name):
    try:
        council_input_data = file_handler.load_inputs_file("input.json")
        context.metadata = council_input_data[council_name]
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        raise (err)

# When we scrape the data from <council> using <selenium_mode> and the <selenium_url> is set.
@when(parsers.parse("we scrape the data from {council} using {selenium_mode} and the {selenium_url} is set"))
def scrape_step(context, council, selenium_mode, selenium_url):
    context.council = council
    context.selenium_mode = selenium_mode
    context.selenium_url = selenium_url

    args = [council, context.metadata["url"]]

    if "uprn" in context.metadata:
        uprn = context.metadata["uprn"]
        args.append(f"-u={uprn}")
    if "postcode" in context.metadata:
        postcode = context.metadata["postcode"]
        args.append(f"-p={postcode}")
    if "house_number" in context.metadata:
        house_number = context.metadata["house_number"]
        args.append(f"-n={house_number}")
    if "usrn" in context.metadata:
        usrn = context.metadata["usrn"]
        args.append(f"-us={usrn}")
    # TODO we should somehow run this test with and without this argument passed
    # TODO I do think this would make the testing of the councils a lot longer and cause a double hit from us

    # At the moment the feature file is set to local execution of the selenium so no url will be set
    # And it the behave test will execute locally
    if selenium_mode != 'None' and selenium_url != 'None':
        if selenium_mode != 'local': 
            web_driver = context.metadata["web_driver"]
            args.append(f"-w={web_driver}")
    if "skip_get_url" in context.metadata:
        args.append(f"-s")

    try:
        CollectData = collect_data.UKBinCollectionApp()
        CollectData.set_args(args)
        context.parse_result = CollectData.run()
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Schema: {err}")
        raise (err)


@then("the result is valid json")
def validate_json_step(context):
    try:
        valid_json = file_handler.validate_json(context.parse_result)
        assert_that(valid_json, True)
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        logging.info(f"JSON Output: {context.parse_result}")
        raise (err)


@then("the output should validate against the schema")
def validate_output_step(context):
    try:
        council_schema = file_handler.load_schema_file(f"output.schema")
        schema_result = file_handler.validate_json_schema(
            context.parse_result, council_schema
        )
        assert_that(schema_result, True)
    except Exception as err:
        logging.error(traceback.format_exc())
        logging.info(f"Validate Output: {err}")
        logging.info(f"JSON Output: {context.parse_result}")
        raise (err)
