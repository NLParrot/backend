# type:ignore
import weaviate
from sentence_transformers import SentenceTransformer


class SingletonModel:
    _instance = None

    @classmethod
    def getInstance(cls):
        if cls._instance == None:
            cls._instance = SentenceTransformer("jhgan/ko-sroberta-multitask")
        return cls._instance


class ChatDB:
    def __init__(self):
        self.connection = weaviate.connect_to_local(port=8080, grpc_port=50051)
        self.embedding_model = SingletonModel.getInstance()

    def __del__(self):
        self.connection.close()

    def query_course(self, course_query):
        course = self.connection.collections.get("CourseName")

        course_vector = self.embedding_model.encode(course_query).tolist()
        course_name = (
            course.query.near_vector(
                near_vector=course_vector,
                limit=1,
            )
            .objects[0]
            .properties["course_name"]
        )

        return course_name

    def query_professor(self, professor_query):
        professor = self.connection.collections.get("ProfessorName")

        professor_vector = self.embedding_model.encode(professor_query).tolist()
        professor_name = (
            professor.query.near_vector(
                near_vector=professor_vector,
                limit=1,
            )
            .objects[0]
            .properties["professor_name"]
        )

        return professor_name

    def query_evaluations(self, keyword_query):
        course_evaluation = self.connection.collections.get("CourseEvaluation")

        keyword_vector = self.embedding_model.encode(keyword_query).tolist()
        evaluations = (
            course_evaluation.query.near_vector(
                near_vector=keyword_vector,
                limit=3,
                filters=wvc.query.Filter.by_property("course_name").equal(course)
                & wvc.query.Filter.by_property("professor_name").equal(professor),
            )
            .objects[0]
            .properties["evaluations"]
        )

        return evaluations

    def query_department_name(self, keyword_query):
        address_location = self.connection.collections.get("AddressLocation")

        keyword_vector = self.embedding_model.encode(keyword_query).tolist()
        department_name = (
            address_location.query.near_vector(near_vector=keyword_vector, limit=3)
            .objects[0]
            .properties["department_name"]
        )

        return department_name

    def query_location_name(self, location_query):
        buildings = self.connection.collections.get("Buildings")

        near_vector = self.embedding_model.encode(location_query).tolist()
        response = buildings.query.near_vector(
            near_vector=near_vector,
            limit=1,
        ).objects[0]

        building_name = response.properties["primary_building_name"]
        coordinates = dict(response.properties["coordinates"])

        return building_name, coordinates
