#include "maze.h"
#include <fcntl.h>
#include "get_next_line.h"
#include <string.h>

/* =========================
   ALLOCATE GRID
   ========================= */

void allocate_grid(t_data *data, int rows, int cols)
{
    int i = 0;

    data->rows = rows;
    data->cols = cols;

    data->grid = malloc(sizeof(t_cell *) * rows);
    if (!data->grid)
        return;

    while (i < rows)
    {
        data->grid[i] = malloc(sizeof(t_cell) * cols);
        i++;
    }
}

/* =========================
   HEX CHAR → INT
   ========================= */

static int hex_to_int(char c)
{
    if (c >= '0' && c <= '9')
        return (c - '0');
    else if (c >= 'A' && c <= 'F')
        return (c - 'A' + 10);
    else if (c >= 'a' && c <= 'f')
        return (c - 'a' + 10);
    else
        return (-1);
}

/* =========================
   PARSE MAZE FILE
   ========================= */

void parse_maze_file(t_data *data, char *filename)
{
    int fd = open(filename, O_RDONLY);
    char *line;
    char **lines;
    int count = 0;

    lines = malloc(sizeof(char *) * 5000);

    /* =========================
       STEP 1: READ ALL LINES
       ========================= */
    while ((line = get_next_line(fd)))
    {
        lines[count++] = line;
    }
    close(fd);

    /* =========================
       STEP 2: FIND GRID END
       (first non-hex line)
       ========================= */
    int grid_end = 0;

    while (grid_end < count)
    {
        if (!lines[grid_end] || !lines[grid_end][0])
        {
            grid_end++;
            continue;
        }

        /* if line contains comma → metadata starts */
        if (strchr(lines[grid_end], ','))
            break;

        grid_end++;
    }

    if (grid_end + 2 >= count)
    {
        write(1, "Invalid maze format\n", 21);
        return;
    }

    /* =========================
       STEP 3: GRID SIZE
       ========================= */
    data->rows = grid_end;
    data->cols = strlen(lines[0]);
    if (lines[0][data->cols - 1] == '\n')
        data->cols--;

    allocate_grid(data, data->rows, data->cols);
    for (int i = 0; i < data->rows; i++)
    {
        for (int j = 0; j < data->cols; j++)
            data->grid[i][j].walls = 0;
    }

    /* =========================
       STEP 4: FILL GRID
       ========================= */
    for (int i = 0; i < data->rows; i++)
    lines[i][strcspn(lines[i], "\n")] = '\0';
    for (int i = 0; i < data->rows; i++)
    {
        for (int j = 0; j < data->cols; j++)
        {
            if (lines[i][j] == '\0')
                data->grid[i][j].walls = 0;
            else
                data->grid[i][j].walls = hex_to_int(lines[i][j]);
        }
    }

    /* =========================
       STEP 5: ENTRY / EXIT / PATH
       ========================= */

    char *entry_line = lines[grid_end];
    char *exit_line  = lines[grid_end + 1];
    char *dir_line   = lines[grid_end + 2];

    /* strip newlines */
    entry_line[strcspn(entry_line, "\n")] = 0;
    exit_line[strcspn(exit_line, "\n")] = 0;
    dir_line[strcspn(dir_line, "\n")] = 0;

    /* ENTRY */
    if (sscanf(entry_line, "%d,%d",
        &data->entry_x, &data->entry_y) != 2)
    {
        write(1, "Invalid entry format\n", 22);
        return;
    }
    data->entry_x -= 1;
    data->entry_y -= 1;

    /* EXIT */
    if (sscanf(exit_line, "%d,%d",
        &data->exit_x, &data->exit_y) != 2)
    {
        write(1, "Invalid exit format\n", 21);
        return;
    }
    data->exit_x -= 1;
    data->exit_y -= 1;

    /* PATH */
    data->path = strdup(dir_line);
    build_path_cells(data);

    /* =========================
       STEP 6: CLEANUP
       ========================= */
    for (int i = 0; i < count; i++)
        free(lines[i]);
    free(lines);
}
