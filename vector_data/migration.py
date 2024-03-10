from tqdm import tqdm

import weaviate

SOURCE_WEAVIATE_URL = "127.0.0.1"
TARGET_WEAVIATE_URL = "175.45.200.101"

client_src = weaviate.connect_to_local()
client_tgt = weaviate.connect_to_local(TARGET_WEAVIATE_URL)


def migrate_data(collection_src, collection_tgt):

    with collection_tgt.batch.fixed_size(batch_size=100) as batch:
        for q in tqdm(collection_src.iterator(include_vector=True)):
            batch.add_object(
                properties=q.properties,
                vector=q.vector["default"],
                uuid=q.uuid
            )

    return True


collections = client_src.collections.list_all()
for k, v in collections:
    reviews_src = client_src.collections.get(k)
    reviews_tgt = client_tgt.collections.get(k)
    migrate_data(reviews_src, reviews_tgt)

client_src.close()
client_tgt.close()
