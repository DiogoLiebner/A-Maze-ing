MLX_DIR := MiniLibX/minilibx-linux
MLX_LIB := $(MLX_DIR)/libmlx.a

C_SRCS:= MiniLibX/MLXmain.c \
		MiniLibX/render.c \
		MiniLibX/parser.c \
		MiniLibX/ft_split.c \
		MiniLibX/get_next_line.c \
		MiniLibX/get_next_line_utils.c

C_INCLUDES:= 	-I MiniLibX -I $(MLX_DIR)
C_FLAGS:=		-Wall -Wextra -Werror
C_LIBS:=		-L$(MLX_DIR) -lmlx -lXext -lX11 -lm

OUTPUT_NAME:=	maze_viewer

VENV:= 		venv
PYTHON:= 	$(VENV)/bin/python3
PIP:=		$(VENV)/bin/pip
MAIN:=		a_maze_ing.py
CONFIG:=	config.txt

all: $(MLX_LIB) $(OUTPUT_NAME) $(VENV)

$(MLX_LIB):
	$(MAKE) -C $(MLX_DIR)

$(OUTPUT_NAME): $(MLX_LIB) $(C_SRCS)
	cc $(C_FLAGS) $(C_INCLUDES) $(C_SRCS) $(C_LIBS) -o $(OUTPUT_NAME)

$(VENV):
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e .
	$(VENV)/bin/pip install flake8 mypy

install: $(VENV)

run: all
	$(PYTHON) $(MAIN) $(CONFIG)

debug: all
	$(PYTHON) -u $(MAIN) $(CONFIG)

clean:
	rm -f $(OUTPUT_NAME)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true

lint:
	$(VENV)/bin/flake8 .
	$(VENV)/bin/mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	$(PYTHON) -m $(PIP) flake8 .
	$(PYTHON) -m $(PIP) mypy . --strict

.PHONY: all install run debug clean lint lint-strict
