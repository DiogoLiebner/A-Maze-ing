#include "maze.h"
#include <string.h>
#include <stdlib.h>

/* =========================
   PIXEL DRAWING
   ========================= */

void put_pixel(t_data *data, int x, int y, int color)
{
    char *dst;

    if (x < 0 || y < 0 || x >= data->win_w || y >= data->win_h)
        return;

    dst = data->addr + (y * data->line_len + x * (data->bpp / 8));

    if (data->path_mode)
        color = 0xFF0000; // 🔴 force red

    *(unsigned int *)dst = color;
}

/* =========================
   LINE DRAWING
   ========================= */

void draw_line(t_data *data, int x1, int y1, int x2, int y2)
{
    int dx = abs(x2 - x1);
    int dy = abs(y2 - y1);
    int steps = (dx > dy) ? dx : dy;

    float x_inc = (steps == 0) ? 0 : (float)(x2 - x1) / steps;
    float y_inc = (steps == 0) ? 0 : (float)(y2 - y1) / steps;

    float x = x1;
    float y = y1;

    for (int i = 0; i <= steps; i++)
    {
        put_pixel(data, (int)x, (int)y, 0xFFFFFF);
        x += x_inc;
        y += y_inc;
    }
}

/* =========================
   CELL FILL
   ========================= */

void fill_cell(t_data *d, int x, int y, int w, int h, int color)
{
    for (int i = 0; i < h; i++)
    {
        for (int j = 0; j < w; j++)
        {
            put_pixel(d, x + j, y + i, color);
        }
    }
}

/* =========================
   PATH CHECK
   ========================= */

int is_on_path(t_data *d, int x, int y)
{
    for (int i = 0; i < d->path_len; i++)
    {
        if (d->path_cells[i].x == x &&
            d->path_cells[i].y == y)
            return 1;
    }
    return 0;
}

/* =========================
   MAIN RENDER
   ========================= */

void render_maze(t_data *d)
{
    int i;
    int j;
    int x;
    int y;
    int walls;

    for (i = 0; i < d->rows; i++)
    {
        for (j = 0; j < d->cols; j++)
        {
            x = j * CELL_SIZE;
            y = i * CELL_SIZE;
            walls = d->grid[i][j].walls;

            /* draw walls */
            if (walls & 1)
                draw_line(d, x, y, x + CELL_SIZE, y);
            if (walls & 2)
                draw_line(d, x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE);
            if (walls & 4)
                draw_line(d, x, y + CELL_SIZE, x + CELL_SIZE, y + CELL_SIZE);
            if (walls & 8)
                draw_line(d, x, y, x, y + CELL_SIZE);
        }
    }

    /* ⭐ PATH IS DRAWN LAST (IMPORTANT) */
    draw_path_line(d);
}

void build_path_cells(t_data *d)
{
    int x = d->entry_x;
    int y = d->entry_y;
    int i = 0;

    int len = strlen(d->path);
    d->path_cells = malloc(sizeof(t_point) * (len + 1));
    d->path_len = 0;

    d->path_cells[d->path_len++] = (t_point){x, y};

    while (d->path[i])
    {
        char c = d->path[i];

        if (c == '\n' || c == '\r' || c == ' ')
        {
            i++;
            continue;
        }

        if (c == 'W')
            x--;
        else if (c == 'E')
            x++;
        else if (c == 'N')
            y--;
        else if (c == 'S')
            y++;
        else
        {
            i++;
            continue;
        }

        /* =========================
           CRITICAL SAFETY CLAMP
           ========================= */
        if (x < 0) x = 0;
        if (y < 0) y = 0;
        if (x >= d->cols) x = d->cols - 1;
        if (y >= d->rows) y = d->rows - 1;

        d->path_cells[d->path_len++] = (t_point){x, y};

        i++;
    }
}

void draw_path_line(t_data *d)
{
    d->path_mode = 1;

    for (int i = 1; i < d->path_len; i++)
    {
        int x1 = d->path_cells[i - 1].x;
        int y1 = d->path_cells[i - 1].y;
        int x2 = d->path_cells[i].x;
        int y2 = d->path_cells[i].y;

        int px1 = x1 * CELL_SIZE + CELL_SIZE / 2;
        int py1 = y1 * CELL_SIZE + CELL_SIZE / 2;

        int px2 = x2 * CELL_SIZE + CELL_SIZE / 2;
        int py2 = y2 * CELL_SIZE + CELL_SIZE / 2;

        draw_line(d, px1, py1, px2, py2);
    }

    d->path_mode = 0;
}

/* =========================
   MAIN RENDER WRAPPER
   ========================= */

void render(t_data *data)
{
    if (data->img)
        mlx_destroy_image(data->mlx, data->img);

    data->img = mlx_new_image(data->mlx, data->win_w, data->win_h);
    data->addr = mlx_get_data_addr(
        data->img,
        &data->bpp,
        &data->line_len,
        &data->endian
    );

    render_maze(data);

    mlx_put_image_to_window(data->mlx, data->win, data->img, 0, 0);
}