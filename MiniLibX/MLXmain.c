#include "maze.h"
#include <stdio.h>

void draw_something(t_data *data)
{
    int i = 0;

    while (i < 300)
    {
        put_pixel(data, i, i, 0x00FF00); // green
        i++;
    }
}

int key_hook(int keycode, void *param)
{
    t_data *data = (t_data *)param;
    printf("KEY: %d\n", keycode);

    if (keycode == 65307) // ESC
    {
        mlx_destroy_window(data->mlx, data->win);
        exit(0);
    }

    if (keycode == 65293) // ENTER → regenerate maze
    {
        system("python3 main.py");

        // free old grid
        for (int i = 0; i < data->rows; i++)
            free(data->grid[i]);
        free(data->grid);
        data->grid = NULL;

        // free old path
        free(data->path);
        free(data->path_cells);
        data->path = NULL;
        data->path_cells = NULL;
        data->path_len = 0;
        data->path_progress = 0;

        // re-parse the new maze file
        parse_maze_file(data, data->filename);

        // resize window if dimensions changed
        int new_w = data->cols * CELL_SIZE;
        int new_h = data->rows * CELL_SIZE;
        if (new_w != data->win_w || new_h != data->win_h)
        {
            data->win_w = new_w;
            data->win_h = new_h;
            mlx_destroy_window(data->mlx, data->win);
            data->win = mlx_new_window(data->mlx, data->win_w, data->win_h, "maze");
            mlx_hook(data->win, 17, 0, close_window, data);
            mlx_key_hook(data->win, key_hook, data);
            mlx_loop_hook(data->mlx, animate, data);
        }

        render(data);
        return (0);
    }

    if (keycode == 32) // spacebar → toggle path
    {
        if (data->path_progress == 0)
            data->path_progress = 1;
        else
            data->path_progress = 0;
        render(data);
    }

    if (keycode == 49) data->wall_color = 0xFFFFFF; // 1 = white
    if (keycode == 50) data->wall_color = 0x870FFF; // 2 = purple
    if (keycode == 51) data->wall_color = 0x00FF00; // 3 = green
    if (keycode == 52) data->wall_color = 0x0000FF; // 4 = blue
    if (keycode == 53) data->wall_color = 0xFFFF00; // 5 = yellow
    if (keycode == 54) data->wall_color = 0xFF00FF; // 6 = magenta
    if (keycode == 55) data->wall_color = 0x00FFFF; // 7 = cyan
    if (keycode == 56) data->wall_color = 0x888888; // 8 = gray
    if (keycode == 57) data->wall_color = 0xFFA500; // 9 = orange

    render(data);
    return (0);
}

int close_window(void *param)
{
    t_data *data = (t_data *)param;

    mlx_destroy_window(data->mlx, data->win);
    exit(0);
    return (0);
}

int main(int argc, char **argv)
{
    t_data data;
    int i, j;

    if (argc != 2)
    {
        write(1, "Usage: ./maze map.txt\n", 23);
        return (1);
    }

    /* =========================
       INIT STRUCT
       ========================= */
    data.mlx = mlx_init();
    data.img = NULL;
    data.grid = NULL;
    data.rows = 0;
    data.cols = 0;
    data.path = NULL;
    data.path_cells = NULL;
    data.path_len = 0;
    data.path_progress = 0;
    data.wall_color = 0xFFFFFF;
    data.filename = argv[1];

    /* =========================
       PARSE FILE (sets rows/cols)
       ========================= */
    parse_maze_file(&data, argv[1]);
    printf("DEBUG → ROWS: %d | COLS: %d\n", data.rows, data.cols);

    /* =========================
       COMPUTE WINDOW SIZE
       ========================= */
    data.win_w = data.cols * CELL_SIZE;
    data.win_h = data.rows * CELL_SIZE;

    /* =========================
       CREATE WINDOW
       ========================= */
    data.win = mlx_new_window(
        data.mlx,
        data.win_w,
        data.win_h,
        "maze"
    );

    /* =========================
       DEBUG OUTPUT
       ========================= */
    printf("ROWS: %d | COLS: %d\n\n", data.rows, data.cols);

    for (i = 0; i < data.rows; i++)
    {
        for (j = 0; j < data.cols; j++)
            printf("%x ", data.grid[i][j].walls);
        printf("\n");
    }

    printf("\n--- launching MLX ---\n");

    /* =========================
       FIRST RENDER
       ========================= */
    render(&data);

    /* =========================
       HOOKS
       ========================= */
    mlx_hook(data.win, 17, 0, close_window, &data);
    mlx_key_hook(data.win, key_hook, &data);

    mlx_loop_hook(data.mlx, animate, &data);
    mlx_loop(data.mlx);

    return (0);
}
