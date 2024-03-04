# type:ignore
import weaviate
import weaviate.classes as wvc
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
        if course_query == None:
            return None

        course = self.connection.collections.get("CourseName")

        course_vector = self.embedding_model.encode(course_query).tolist()
        course_name = course.query.hybrid(
            query=course_query,
            vector=course_vector,
            limit=1,
        ).objects

        if len(course_name) == 0:
            return None

        course_name = course_name[0].properties["course_name"]

        return course_name

    def query_professor(self, professor_query):
        if professor_query == None:
            return None

        professor = self.connection.collections.get("ProfessorName")

        professor_vector = self.embedding_model.encode(professor_query).tolist()
        professor_name = professor.query.hybrid(
            query=professor_query,
            vector=professor_vector,
            limit=1,
        ).objects

        if len(professor_name) == 0:
            return None

        professor_name = professor_name[0].properties["professor_name"]

        return professor_name

    def query_course_professor(self, course_name, professor_name):
        if course_name == None or professor_name == None:
            return None, None

        professor_vector = self.embedding_model.encode(professor_name)
        course_vector = self.embedding_model.encode(course_name)
        course_col = self.connection.collections.get("Course")
        result = course_col.query.near_vector(
            near_vector=((professor_vector + course_vector) / 2).tolist(), limit=1
        ).objects

        if len(result) == 0:
            course = self.query_course(course_name)
            professor = self.query_professor(professor_name)
            return course, professor

        return (
            result[0].properties["course_name"],
            result[0].properties["professor_name"],
        )

    def query_evaluations(self, course, professor, keyword_query):
        if any(k == None for k in (course, professor, keyword_query)):
            return None

        course, professor = self.query_course_professor(course, professor)
        if course == None or professor == None:
            return None

        course_evaluation = self.connection.collections.get("CourseEvaluation")

        keyword_vector = self.embedding_model.encode(keyword_query).tolist()
        evaluations = course_evaluation.query.hybrid(
            query=keyword_query,
            vector=keyword_vector,
            limit=3,
            filters=wvc.query.Filter.by_property("course_name").equal(course)
            & wvc.query.Filter.by_property("professor_name").equal(professor),
        ).objects

        if len(evaluations) == 0:
            return None

        evaluations = [x.properties["evaluations"] for x in evaluations]

        return evaluations

    def query_department_name(self, keyword_query):
        if keyword_query == None:
            return None

        address_location = self.connection.collections.get("AddressLocation")

        keyword_vector = self.embedding_model.encode(keyword_query).tolist()
        department_name = address_location.query.hybrid(
            query=keyword_query, vector=keyword_vector, limit=1
        ).objects

        if len(department_name) == 0:
            return None

        department_name = department_name[0].properties["department_name"]

        return department_name

    def query_location_name(self, location_query):
        if location_query == None:
            return None, None

        buildings = self.connection.collections.get("Buildings")

        near_vector = self.embedding_model.encode(location_query).tolist()
        response = buildings.query.hybrid(
            query=location_query,
            vector=near_vector,
            limit=1,
        ).objects

        if len(response) == 0:
            return None

        response = response[0]

        building_name = response.properties["primary_building_name"]
        coordinates = dict(response.properties["coordinates"])

        return building_name, coordinates


if __name__ == "__main__":
    c = ChatDB()
    print(c.query_professor("소정민"))
