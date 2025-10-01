from fastapi import FastAPI
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import uvicorn, pandas as pd

class RecomendationSystem:
    def __init__(self):
        self.df_films_reviews = self.load_dataset()
        self.users_pivot = self.create_users_pivot(self.df_films_reviews)
        self.film_df_matrix = self.create_csr_matrix(self.users_pivot)

    def load_dataset(self) -> pd.DataFrame:
        return pd.read_csv('datasets/df_films_reviews.csv')
    
    def create_users_pivot(self, df_films_reviews: pd.DataFrame) -> pd.DataFrame:
        new_df = df_films_reviews[(df_films_reviews['userId'].map(df_films_reviews['userId'].value_counts()) > 1000) | (df_films_reviews['userId'] == 222333)]
        users_pivot=new_df.pivot_table(index=["userId"],columns=["title"],values="rating")
        users_pivot.fillna(0,inplace=True)
        return users_pivot
    
    def create_csr_matrix(self, users_pivot: pd.DataFrame) -> csr_matrix:
        return csr_matrix(users_pivot.values)

    def popularite_films(self) -> dict:
        avg_ratings = self.df_films_reviews.groupby('title')['rating'].mean().reset_index().rename(columns={'rating': 'avg_rating'})
        avg = pd.DataFrame(avg_ratings).sort_values('avg_rating',ascending=False)
        cnt_ratings = self.df_films_reviews.groupby('title')['rating'].count().reset_index().rename(columns={'rating': 'count_rating'})
        cnt=pd.DataFrame(cnt_ratings).sort_values('count_rating',ascending=False)
        popularite=avg.merge(cnt,on='title')
        v=popularite["count_rating"]
        R=popularite["avg_rating"]
        m=v.quantile(0.90)
        c=R.mean()
        popularite['w_score']=((v*R) + (m*c)) / (v+m)
        return popularite.sort_values('w_score',ascending=False).head(10).reset_index()[['title', 'w_score']]
    
    def popularite_films_by_genre(self, genre: str) -> pd.DataFrame:
        df = self.df_films_reviews[self.df_films_reviews['genres'] == genre]
        avg_ratings = df.groupby('title')['rating'].mean().reset_index().rename(columns={'rating': 'avg_rating'})
        avg = pd.DataFrame(avg_ratings).sort_values('avg_rating',ascending=False)
        cnt_ratings = df.groupby('title')['rating'].count().reset_index().rename(columns={'rating': 'count_rating'})
        cnt=pd.DataFrame(cnt_ratings).sort_values('count_rating',ascending=False)
        popularite=avg.merge(cnt,on='title')
        v=popularite["count_rating"]
        R=popularite["avg_rating"]
        m=v.quantile(0.90)
        c=R.mean()
        popularite['w_score']=((v*R) + (m*c)) / (v+m)
        return popularite.sort_values('w_score',ascending=False).head(10).reset_index()[['title', 'w_score']]
    
    def same_films(self, name_film):
        users_vote_film=self.users_pivot[name_film]
        similar_with=self.users_pivot.corrwith(users_vote_film)
        similar_with = pd.DataFrame({'title' : similar_with.to_dict().keys(), 'correlation' : similar_with.to_dict().values()})
        df=similar_with.sort_values('correlation',ascending=False).reset_index(drop=True).iloc[1:11]
        return df
    
    def find_favorite_films(self, User_id, num_books=10):
        model_knn = NearestNeighbors(metric='cosine', algorithm='brute')
        model_knn.fit(self.film_df_matrix)
        
        user_index = self.users_pivot.index.get_loc(User_id)
        
        distances, indices = model_knn.kneighbors(self.film_df_matrix[user_index], n_neighbors=num_books+1)

        favorite_indices = indices[0][1:]
        favorite_distances = distances[0][1:]


        list_favorite_films = [self.users_pivot.columns[idx] for idx in favorite_indices]
        favorite_films=pd.DataFrame({"favorite films ":list_favorite_films, "distances" : favorite_distances})
        return favorite_films
    
    def genre_films(self):
        return self.df_films_reviews['genres'].unique().tolist()
    
    def name_films(self):
        return self.df_films_reviews['title'].unique().tolist()

    def users_id(self):
        new_df = self.df_films_reviews[(self.df_films_reviews['userId'].map(self.df_films_reviews['userId'].value_counts()) > 1000) | (self.df_films_reviews['userId'] == 222333)]
        return new_df.userId.unique().tolist()

app = FastAPI()
recomendation_system = RecomendationSystem()

@app.get('/get_popularite_films')
def get_popularite_films():
    return recomendation_system.popularite_films()

@app.get('/get_popularite_films_by_genre/{genre}')
def get_popularite_films_by_genre(genre: str):
    return recomendation_system.popularite_films_by_genre(genre)

@app.get('/get_same_films_by_name/{name_film}')
def get_same_films_by_name(name_film: str):
    return recomendation_system.same_films(name_film)

@app.get('/get_favorite_films/{user_id}')
def get_favorite_films(user_id: int):
    return recomendation_system.find_favorite_films(user_id)

@app.get('/get_genre_films/')
def get_genre_films():
    return recomendation_system.genre_films()

@app.get('/get_name_films/')
def get_name_films():
    return recomendation_system.name_films()

@app.get('/get_users_id/')
def get_users_id():
    return recomendation_system.users_id()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)