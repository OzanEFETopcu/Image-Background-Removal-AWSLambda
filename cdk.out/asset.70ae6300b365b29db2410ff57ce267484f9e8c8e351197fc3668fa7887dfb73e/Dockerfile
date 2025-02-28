FROM public.ecr.aws/lambda/python:3.12
COPY requirements.txt ${LAMBDA_TASK_ROOT}
ENV NUMBA_CACHE_DIR="/tmp/"
ENV U2NET_HOME="/tmp"
RUN pip install -r requirements.txt
COPY src/* ${LAMBDA_TASK_ROOT}
CMD [ "main.lambda_handler" ]

