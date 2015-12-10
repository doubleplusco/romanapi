import romanify
import logging
import json

def convert (value, context):
    # log in json format for easy ingestion in log management tools
    FORMAT = '{'
    FORMAT += '"@timestamp":"%(asctime)s","level":"%(levelname)s","message":"%(message)s"'
    FORMAT += ',"aws_request_id":"' + context.aws_request_id + '"'
    FORMAT += ',"function_version":"' + context.function_version + '"'
    FORMAT += ',"function_arn":"' + context.invoked_function_arn + '"'
    FORMAT += ',"log_group_name":"' + context.log_group_name + '"'
    FORMAT += ',"log_stream_name":"' + context.log_stream_name + '"'
    FORMAT += '}'

    # set the date format to ISO 8601
    DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"

    logging.basicConfig(format=FORMAT, datefmt=DATE_FORMAT, level=logging.INFO)

    # create logger
    logger = logging.getLogger("RomanAPI")

    # create console handler and set level to info
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)

    # create formatter
    formatter = logging.Formatter(fmt=FORMAT, datefmt=DATE_FORMAT)

    # add formatter to ch
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(ch)

    # initialise defaults
    arabic = roman = result = error = None

    try:
        logger.info("received input: '%s'" % value)

        # input comes in as a string with potential spaces
        numeral = value.strip()

        # reject invalid which are not handled by the library
        if numeral in [None, "", "0"] or numeral.startswith("-"):
            error = "invalid numeral: please provide a roman or positive arabic numeral"
        else:
            # first, assume the numeral is arabic
            try:
                logger.info({"message": "Attempting to cast numeral to integer"})
                arabic = int(numeral)

                # so far so good, assume this is an arabic numeral
                try:
                    logger.info({"message": "attempting to convert numeral from arabic to roman"})
                    result = roman = "%s" % romanify.arabic2roman(arabic)
                except ValueError as e:
                    # something went wrong, log the error and assume this a roman numeral
                    error = "invalid numeral: %s" % e

            # failing that, assume the numeral is roman
            except:
                try:
                    logger.info({"message": "attempting to convert numeral from roman to arabic"})
                    roman = numeral

                    result = arabic = romanify.roman2arabic(numeral)
                except ValueError as e:
                    # ok, the numeral is neither valid arabic nor roman
                    error = "invalid numeral: %s" % e

    # catch all other exceptions
    except Exception as e:
        error = str(e)
    finally:
        if error is not None:
            raise Exception(error)
        else:
            response = { "success": True, "arabic": arabic, "roman": roman, "original": numeral, "result": result }
            return response

        logger.info(json.dumps(response))

# need this for local testing
if __name__ == "__main__":
    import sys

    # mock aws context object
    class MockContext(object):
        aws_request_id = "12345"
        function_version = "50"
        invoked_function_arn = "function:roman_api_convert"
        log_group_name = "log_group"
        log_stream_name = "log_stream"

    mock_context = MockContext()

    numeral = sys.argv[1]
    print(convert(numeral, mock_context))