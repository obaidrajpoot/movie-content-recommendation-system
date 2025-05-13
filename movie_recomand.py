from flask import Flask,request,render_template
import pickle
import pandas as pd
import numpy as np
movie_data = pickle.load(open('movies_data.pkl','rb'))
movie_similarity_score = pickle.load(open('cosine_scores.pkl','rb'))
app = Flask(__name__)
@app.route('/',methods=['GET','POST'])
def movie_recomand():
    if request.method == 'POST':
        movie_name = request.form.get('movie').strip()
        movie_name = movie_name.lower()
        movie_index = movie_data[movie_data['title']==movie_name].index[0]
        similar_movie = list(enumerate(movie_similarity_score[movie_index]))
        sorted_similar_movies = sorted(similar_movie, key=lambda x: x[1], reverse=True)[1:6]
        temp_data=[]
        for i in sorted_similar_movies:
            temp=movie_data.iloc[i[0]]
            temp_store={
                 'title': temp['title'],
                 'vote_average': temp['vote_average'].item(),
                 'status': temp['status'],
                 'release_date': temp['release_date'],
                 'revenue': temp['revenue'].item(),
                 'runtime': temp['runtime'].item(),
                 'adult': temp['adult'],
                 'budget': temp['budget'],
                 'original_language': temp['original_language'],
                 'overview': temp['overview'],
                 'vote_count': temp.get('vote_count', 0),
                 'popularity': temp.get('popularity', 0),
                 'image': temp.get('image_path', '') 
            }
            
            temp_data.append(temp_store)
        
        return render_template('content_recommand.html', data=temp_data, movie_name=movie_name)

    # Render empty recommend form on GET
    return render_template('content_recommand.html')

if __name__=='__main__':
    app.run(debug=True)