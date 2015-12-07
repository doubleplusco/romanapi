import romanify
import logging
import json

def convert (value, context):
    # log in json format for easy ingestion in log management tools
    FORMAT = '{"@timestamp":"%(asctime)s","level":"%(levelname)s","aws_request_id":"' + context.aws_request_id + '","message":"%(message)s"}'
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
    arabic = roman = error = None

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
                    roman = "%s" % romanify.arabic2roman(arabic)
                except ValueError as e:
                    # something went wrong, log the error and assume this a roman numeral
                    error = "invalid numeral: %s" % e

            # failing that, assume the numeral is roman
            except:
                try:
                    logger.info({"message": "attempting to convert numeral from roman to arabic"})
                    roman = numeral

                    arabic = romanify.roman2arabic(numeral)
                except ValueError as e:
                    # ok, the numeral is neither valid arabic nor roman
                    error = "invalid numeral: %s" % e

    # catch all other exceptions
    except Exception as e:
        error = str(e)
    finally:
        if error is None:
            response = { "success": True, "arabic": arabic, "roman": roman}
        else:
            response = { "success": False, "message": error }

        logger.info(json.dumps(response))
        return response

# need this for local testing
if __name__ == "__main__":
    import sys

    # mock aws context object
    class MockContext(object):
        aws_request_id = "mock_123456"

    mock_context = MockContext()

    numeral = sys.argv[1]
    print(convert(numeral, mock_context))