from system.core.model import Model
import re

class like(Model):
    def __init__(self):
        super(like, self).__init__()
    def create(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []
        
        if len(info['name']) < 2:
            errors.append('Name needs to be at least 2 characters long')
        if len(info['alias']) < 2:
            errors.append('Alias needs to be at least 2 characters long')
        if not info['email']:
            errors.append('Email can\'t be blank')
        elif not EMAIL_REGEX.match(info['email']):
            errors.append('Email must be in valid format')
        if len(info['password']) < 3:
            errors.append('Password must be longer than 3 characters')
        if info['password'] != info['confirm_password']:
            errors.appened('Password doesn\'t match')
        
        if errors:
            return {"status" :False, 'errors' :errors}
        else:
            pw_hash = self.bcrypt.generate_password_hash(info['password'])
            create_user_query = "INSERT INTO users (name, alias, email, password,created_at, updated_at) VALUES ('{}', '{}', '{}', '{}', NOW(), NOW())".format(info['name'], info['alias'], info['email'],pw_hash)
            self.db.query_db(create_user_query)
            return {"status":True}
    def login(self, info):
        EMAIL_REGEX = re.compile(r'^[a-za-z0-9\.\+_-]+@[a-za-z0-9\._-]+\.[a-za-z]*$')
        errors = []

        if not info['login_email']:
            errors.append('Email can\'t be blank')
        elif not EMAIL_REGEX.match(info['login_email']):
            errors.append('Email must be in valid format')
        if len(info['login_password']) < 3:
            errors.append('Incorrect password/email')
        if errors:
            return {'status':False, 'errors':errors}
        else:
            user_info_query = "SELECT * FROM users WHERE email = '{}' LIMIT 1".format(info['login_email'])
            user_info = self.db.query_db(user_info_query)
            print user_info

            if user_info:
                if self.bcrypt.check_password_hash(user_info[0]['password'], info['login_password']):
                    return {'status':True, 'login':user_info[0]}
                else:
                    errors.append('Incorrect password/email')
                    return {'status':False, 'errors':errors }
            else:
                errors.append('Incorrect password/email')
                return {'status':False, 'errors':errors}

    def add_post(self, info):
        add_post_query = "INSERT INTO posts (message, user_id, created_at, updated_at) VALUES ('{}','{}',NOW(),NOW())".format(info['post'], info['user_id'])
        self.db.query_db(add_post_query)
        return True
    def all_posts(self):
        all_posts_query = "SELECT users.id AS user_id,posts.message AS message, users.alias, posts.id AS post_id, COUNT(likes.user_id) AS count FROM users JOIN posts ON users.id = posts.user_id LEFT JOIN likes ON posts.id = likes.post_id GROUP BY posts.id ORDER BY count DESC"
        all_posts = self.db.query_db(all_posts_query)
        print all_posts
        return all_posts
    def add_like(self,id, info):
        add_like_query = "INSERT INTO likes (user_id, post_id, created_at, updated_at) VALUES ('{}','{}', NOW(), NOW())".format(id, info['post_id'])
        self.db.query_db(add_like_query)
        return True
    def profile_info(self, id):
        profile_info_query = "SELECT * FROM users WHERE id = '{}'".format(id)
        profile_info = self.db.query_db(profile_info_query)

        total_post_query = "SELECT COUNT(posts.id) AS count FROM users LEFT JOIN posts ON users.id = posts.user_id WHERE users.id = '{}'".format(id)
        total_post = self.db.query_db(total_post_query)

        total_likes_query = "SELECT COUNT(likes.user_id) AS count FROM users LEFT JOIN likes ON  users.id = likes.user_id WHERE users.id = '{}'".format(id)
        total_likes = self.db.query_db(total_likes_query)
        print {'profile':profile_info}
        return {'profile':profile_info[0], 'likes':total_likes[0], 'posts':total_post[0]}

    def post_info(self, id):
        post_info_query = "SELECT users.alias, posts.message, users.id FROM users JOIN posts ON users.id = posts.user_id WHERE posts.id = '{}'".format(id)
        post_info = self.db.query_db(post_info_query)

        like_info_query = "SELECT DISTINCT users.id, users.alias, users.name FROM users  JOIN likes ON users.id = likes.user_id WHERE likes.post_id = '{}'".format(id)
        like_info = self.db.query_db(like_info_query)

        return {'post':post_info[0], 'likes':like_info}

    def delete_post(self, id):
        delete_likes_query = "DELETE FROM likes WHERE post_id = '{}'".format(id)
        delete_likes = self.db.query_db(delete_likes_query)

        delete_post_query = "DELETE FROM posts WHERE id = '{}'".format(id)
        delete_post = self.db.query_db(delete_post_query)
        return True