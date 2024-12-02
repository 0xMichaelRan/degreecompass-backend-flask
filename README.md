# 写在前面

本项目是degree-compass的backend，使用flask框架。

于2024年12月2日开源老代码，并移入我的私有repo继续商业化开发。

希望对大家有帮助！

# Setup

Use poetry to manage dependencies:

```
poetry new flask-degree-compass
cd flask-degree-compass
poetry add flask
vi app.py
poetry run python app.py 
```

## Pending features

* User login and register. 
* Improve LLM support for major details page. 
* CI/CD pipeline. 
* Dockerize the app. 