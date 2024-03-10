import weaviate
import weaviate.classes as wvc
import weaviate.classes.config as wvcc

client = weaviate.connect_to_local(
    port=8080,
    grpc_port=50051,
)

if (client.collections.exists("CourseName")):
  client.collections.delete("CourseName")  
if (client.collections.exists("ProfessorName")):
  client.collections.delete("ProfessorName") 
if (client.collections.exists("Course")):
  client.collections.delete("Course") 
if (client.collections.exists("CourseEvaluation")):
  client.collections.delete("CourseEvaluation")  
if (client.collections.exists("AddressLocation")):
  client.collections.delete("AddressLocation")
if (client.collections.exists("Buildings")):
  client.collections.delete("Buildings")  



client.collections.create("CourseName",
                          properties=[
                              wvcc.Property(name="course_name", data_type=wvcc.DataType.TEXT)
                          ])
client.collections.create("ProfessorName",
                          properties=[
                              wvcc.Property(name="professor_name", data_type=wvcc.DataType.TEXT)
                          ])
                          
client.collections.create("Course",
                         properties=[
                             wvcc.Property(name="course_name", data_type=wvcc.DataType.TEXT),
                             wvcc.Property(name="professor_name", data_type=wvcc.DataType.TEXT)
                         ])
client.collections.create("CourseEvaluation",
                          properties=[
                              wvcc.Property(
                                  name="evaluations", 
                                  data_type=wvcc.DataType.TEXT,
                              ),
                              wvcc.Property(
                                  name="course_name", 
                                  data_type=wvcc.DataType.TEXT,
                              ),
                              wvcc.Property(
                                  name="professor_name", 
                                  data_type=wvcc.DataType.TEXT,
                              )
                          ],
                          references=[
                              wvcc.ReferenceProperty(
                                  name="course",
                                  target_collection="Course"
                              ),
                          ])


client.collections.create("AddressLocation",
                          properties=[
                              wvcc.Property(name="department_name", data_type=wvcc.DataType.TEXT)
                          ])

client.collections.create("Buildings",
                          properties=[
                              wvcc.Property(name="primary_building_name", data_type=wvcc.DataType.TEXT),
                              wvcc.Property(name="building_name", data_type=wvcc.DataType.TEXT),
                              wvcc.Property(name="coordinates", data_type=wvcc.DataType.GEO_COORDINATES)
                          ])

client.close()
