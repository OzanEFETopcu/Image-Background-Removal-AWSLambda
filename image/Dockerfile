FROM public.ecr.aws/lambda/python:3.9
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --target "${LAMBDA_TASK_ROOT}"
RUN mkdir .u2net && curl -L https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -o .u2net/u2net.onnx
ENV U2NET_HOME="${LAMBDA_TASK_ROOT}/.u2net/"
ENV NUMBA_CACHE_DIR="/tmp/"
COPY src/* ${LAMBDA_TASK_ROOT}
CMD [ "main.lambda_handler" ]
