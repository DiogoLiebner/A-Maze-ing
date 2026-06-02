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

    // ❌ ESC (Linux version)
    if (keycode == 65307)
    {
        mlx_destroy_window(data->mlx, data->win);
        exit(0);
    }

    if (keycode == 49) data->wall_color = 0xFFFFFF; // 1 = white
    if (keycode == 50) data->wall_color = 0x870FFF; // 2 = red
    if (keycode == 51) data->wall_color = 0x00FF00; // 3 = green
    if (keycode == 52) data->wall_color = 0x0000FF; // 4 = blue
    if (keycode == 53) data->wall_color = 0xFFFF00; // 5 = yellow
    if (keycode == 54) data->wall_color = 0xFF00FF; // 6 = magenta
    if (keycode == 55) data->wall_color = 0x00FFFF; // 7 = cyan
    if (keycode == 56) data->wall_color = 0x888888; // 8 = gray
    if (keycode == 57) data->wall_color = 0xFFA500; // 9 = orange

    if (keycode == 65361) data->x -= 10; // left
    if (keycode == 65363) data->x += 10; // right
    if (keycode == 65364) data->y += 10; // down
    if (keycode == 65362) data->y -= 10; // up

    // 🔄 redraw
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

void draw_circle(t_data *data, int cx, int cy, int r, int color)
{
    int x, y;

    for (x = -r; x <= r; x++)
    {
        for (y = -r; y <= r; y++)
        {
            if (x*x + y*y <= r*r)
                put_pixel(data, cx + x, cy + y, color);
        }
    }
}

/*int main(void)
{
    t_data data;
    data.x = WIDTH / 2;
    data.y = HEIGHT / 2;


    data.mlx = mlx_init();
    data.win = mlx_new_window(data.mlx, WIDTH, HEIGHT, "MLX Test");

    data.img = mlx_new_image(data.mlx, WIDTH, HEIGHT);
    data.addr = mlx_get_data_addr(
        data.img,
        &data.bpp,
        &data.line_len,
        &data.endian
    );

    draw_circle(&data, 100, 100, 50, 0xFF0000);

    mlx_put_image_to_window(data.mlx, data.win, data.img, 0, 0);

    mlx_key_hook(data.win, key_hook, &data);
    mlx_hook(data.win, 17, 0, close_window, &data);

    mlx_loop(data.mlx);
}*/

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
    data.path_progress = 1;
    data.wall_color = 0xFFFFFF;

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
       CREATE WINDOW (NOW SAFE)
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
