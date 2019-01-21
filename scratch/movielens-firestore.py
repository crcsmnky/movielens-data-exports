from google.cloud import firestore
from pymongo import MongoClient

BATCH_SIZE = 500

def main():
    mdb = MongoClient()['movieweb']
    fdb = firestore.Client()

    total = mdb.movies.count_documents({})

    for i in xrange(0, total, BATCH_SIZE):
        movies = mdb.movies.find().skip(i).limit(BATCH_SIZE)
        batch = fdb.batch()
        
        for m in movies:
            movieid = m['movieid']
            del m['_id']
            # del m['movieid']
            
            movieref = fdb.collection('movies').document(str(movieid))
            batch.set(movieref, m)
        
        batch.commit()
        print('docs inserted: {} - {}'.format(i, i + BATCH_SIZE))

    # genres = mdb.genres.find()

    # for g in genres:
    #     genreid = g['name']
    #     del g['_id']
    #     genreref = fdb.collection('genres').document(genreid)
    #     genreref.set(g)


if __name__ == "__main__":
    main()