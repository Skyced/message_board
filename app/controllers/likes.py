from system.core.controller import *
from flask import redirect, request, flash

class likes(Controller):
    def __init__(self,action):
        super(likes, self).__init__(action)
        self.load_model('like')

    def index(self):
        return self.load_view('/index.html')

    def create(self):
        user_info = request.form
        user = self.models['like'].create(user_info)
        if user['status'] == False:
            for message in user['errors']:
                flash(message)
                return redirect('/')
        else:
            flash("You have succesfully registered!")
            return redirect('/')

    def login(self):
        user_info = request.form
        user = self.models['like'].login(user_info)
        if user['status'] == True:
            session['id'] = user['login']['id']
            session['alias'] = user['login']['alias']
            return redirect('/bright_ideas')
        else:
            for message in user['errors']:
                flash(message)
                return redirect('/')
    def home(self):
        all_posts = self.models['like'].all_posts()
        return self.load_view('/home.html', all_posts = all_posts)

    def post(self):
        post_info = request.form
        post = self.models['like'].add_post(post_info)
        return redirect('/bright_ideas')

    def like(self):
        user_id = session['id']
        like_info = request.form
        like = self.models['like'].add_like(user_id, like_info)
        return redirect('/bright_ideas')

    def profile(self, id):
        user_id = id
        profile_info = self.models['like'].profile_info(user_id)
        return self.load_view('/profile.html',profile_info=profile_info)

    def post_info(self, id):
        post_id = id
        post_info = self.models['like'].post_info(post_id)
        return self.load_view('/post_info.html', post_info = post_info)

    def logout(self):
        session.pop = ['id']
        session.pop = ['alias']
        return redirect('/')

    def delete(self, id):
        post_id = id
        delete_post = self.models['like'].delete_post(post_id)
        return redirect('/bright_ideas')