<p align="center"><img src='./images/logo.webp'/></p>

# AI Trace
AI Trace: Track, log, and evaluate AI models. Supports OpenAI, Claude, Google API and custom PyTorch models.<br/>
Our goal is to make llm application more valuable and effortlessly improve llm capabilities.

# Quickstart
AITrace is composed by three parts - web, backend crud python-sdk and kubent.
## Deployment
First build docker image.
```docker
docker build -t aitrace-backend .
docker build --target web-runtime -t aitrace-web .
docker build --target postgres -t aitrace-postgres .
```
Then run docker container
```docker
docker run -d --name aitrace-postgres -p 16432:5432 -v aitrace_pgdata:/var/lib/postgresql/data aitrace-postgres
docker run -d --name aitrace-web -p 5173:80 -e BACKEND_HOST=host.docker.internal aitrace-web
docker run -d --name aitrace-backend -e DB_URL=jdbc:postgresql://host.docker.internal:16432/aitrace -p 8080:8080 aitrace-backend
```
## Python-sdk
[Click here](src/README.md)

# Development
AT project package manager is uv. If you are a beginner uver, please click uv link: [uv official link](https://docs.astral.sh/uv/guides/projects/#creating-a-new-project)
```bash
cd src
uv install
uv .venv/Script/activate
```
You can watch more detailed debug information by using `--log-level=DEBUG` or `set AT_LOG_LEVEL=DEBUG` for Windows or `export AT_LOG_LEVEL=DEBUG` for Linux and Mac.