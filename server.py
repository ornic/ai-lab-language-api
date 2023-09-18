from aiohttp import web
import multiprocessing
import fasttext
import json
import gcld3
import pycld2 as cld2
from graylog import netlog_info, netlog_error


model = None
detector = None


def isModelLoaded():
    return not ((model is None) or (detector is None))


def loadModel():
    global model
    model = fasttext.load_model("./models/lid.176.bin")
    global detector
    detector = gcld3.NNetLanguageIdentifier(min_num_bytes=0, max_num_bytes=1000)


async def healthcheck(request):
    try:
        if not isModelLoaded():
            loadModel()

        return web.Response(text="pong")

    except Exception as e:
        return web.Response(text="Error type: " + str(type(e)), status=500)


async def about(request):
    if not isModelLoaded():
        loadModel()

    text = (
        "Server: Gunicorn. CPU count: "
        + str(multiprocessing.cpu_count())
        + ". FastText model words count: "
        + str(len(model.words))
        + "."
    )
    return web.Response(text=text)


async def post_language(request):
    try:
        if not isModelLoaded():
            loadModel()

        data = await request.json()
        text = data["text"]

        print("Got text to detect language: [" + text + "]", flush=True)

        output = model.predict(text, 1)
        language = output[0][0].replace("__label__", "")
        print("Fasttext result: [" + language + "]", flush=True)

        result = detector.FindLanguage(text=text)
        print("CLD3 result: [" + result.language + "]", flush=True)

        isReliable, textBytesFound, details = cld2.detect(text)
        print("CLD2 result: [" + details[0][1] + "]", flush=True)

        variants = {language, result.language}
        if isReliable:
            variants.add(details[0][1])

        if len(variants) > 1:
            raise ValueError(
                "Fasttext language detected: "
                + language
                + ", but cld3 found: "
                + result.language
                + ", and cld2 answered: "
                + details[0][1]
            )

        res = {"language": language}
        netlog_info(
            "Detected language for text [" + text + "] is [" + language + "]", ""
        )
    except Exception as e:
        netlog_error(str(e), "")
        res = {"language": "n/a", "error": str(e)}
    return web.json_response(res)


app = web.Application()
app.router.add_get("/", about)
app.router.add_get("/ping", healthcheck)
app.router.add_post("/language", post_language)

print("starting [" + __name__ + "]", flush=True)

if __name__ == "__main__":
    loadModel()
    web.run_app(app, port=8000)
