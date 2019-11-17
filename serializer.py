from constants import Constants


class Serializer:

    @staticmethod
    def deserialize_params(input_str: str):
        return tuple(input_str.split(Constants.SEPARATOR))

    @staticmethod
    def serialize_response(feedback: str, params: list):
        output = feedback + Constants.SEPARATOR
        length = len(params)
        for i in range(length):
            output += str(params[i])
            if i < length - 1:
                output += Constants.SEPARATOR
        return output

