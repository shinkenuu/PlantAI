def load_ollama_model(model_name: str = "model.pb", onnx_file_name: str = "model.onnx"):
    import ollama

    model = ollama.load_model(model_name)
    onnx_model = ollama.export_onnx(model, onnx_file_name)
    return onnx_model


# ============= ONNX ============= #


def load_transformers_model(
    model_name: str = "zephyr-beta", onnx_file_name: str = "model.onnx"
):
    import transformers

    model = transformers.AutoModel.from_pretrained(model_name)
    onnx_model = transformers.onnx.convert_model(model, onnx_file_name)
    return onnx_model


# ============= PROFILING ============= #


def profile(session: "rknn.Session" = None):
    import rknn

    session = session or rknn.Session()
    session.load("model.onnx")
    context = session.get_context("profiling")

    context.start()
    session.run()
    context.stop()

    report = session.get_report("profiling")
    print(report)
    return session


# ============= OPTIMIZATION ============= #


def profile(session: "rknn.Session" = None):
    import rknn

    session = session or rknn.Session()
    session.load("model.onnx")

    options = {
        "fusion": True,
        "loop_optimization": True,
        "memory_management": True,
    }

    session.optimize(options=options)
    session.save("model_optimized.onnx")
    return session


# ============= COMPILATION ============= #


def compile(
    session: "rknn.Session" = None, target: str = "rk3588", device: str = "rk3588-xu"
):
    import rknn

    session = session or rknn.Session()
    session.load("model_optimized.onnx")

    session.compile(target=target, device=device)
    session.save("model_compiled.rknn")
    return session
