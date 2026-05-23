#include "maze.h"

void put_pixel(t_data *data, int x, int y, int color)
{
    char *dst;

    if (x < 0 || y < 0 || x >= WIDTH || y >= HEIGHT)
        return;

    dst = data->addr
        + (y * data->line_len + x * (data->bpp / 8));

    *(unsigned int *)dst = color;
}

void draw_something(t_data *data)
{
    int i = 0;

    while (i < 300)
    {
        put_pixel(data, i, i, 0x00FF00); // green
        i++;
    }
}

int key_hook(int keycode, void * param)
{
    t_data *data = (t_data *)param;

    if (keycode == 53) // ESC on macOS
    {
        mlx_destroy_window(data->mlx, data->win);
        exit(0);
    }

    if (keycode == 65361) // left arrow
        data->x -= 10;
    if (keycode == 65363) // right arrow
        data->x += 10;
    if (keycode == 65364) // down arrow
        data->y += 10;
    if (keycode == 65362) // up arrow
        data->y -= 10;

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

void render(t_data *data)
{
    // clear screen (simple way: recreate image)
    data->img = mlx_new_image(data->mlx, WIDTH, HEIGHT);
    data->addr = mlx_get_data_addr(data->img,
        &data->bpp, &data->line_len, &data->endian);

    draw_circle(data, data->x, data->y, 20, 0xFF0000);

    mlx_put_image_to_window(data->mlx, data->win, data->img, 0, 0);
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

int main(void)
{
    t_data data;

    data.mlx = mlx_init();
    data.win = mlx_new_window(data.mlx, WIDTH, HEIGHT, "MLX Circle Move");

    data.x = WIDTH / 2;
    data.y = HEIGHT / 2;

    render(&data);

    mlx_key_hook(data.win, key_hook, &data);
    mlx_hook(data.win, 17, 0, close_window, &data);

    mlx_loop(data.mlx);

    return (0);
}
