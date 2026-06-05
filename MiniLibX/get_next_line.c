/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: rafmonte <rafmonte@student.42porto.com>    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/06 17:46:32 by rafmonte          #+#    #+#             */
/*   Updated: 2026/01/10 14:36:46 by rafmonte         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"
#include <fcntl.h>
#include <stdio.h>

char	*ft_free(char *old, char *buf)
{
	char	*temp;

	temp = ft_strjoin(old, buf);
	free(old);
	return (temp);
}

char	*ft_next(char *buffer)
{
	int		i;
	int		j;
	char	*next;	

	i = 0;
	j = 0;
	while (buffer[i] && buffer[i] != '\n')
		i++;
	if (!buffer[i])
	{
		free(buffer);
		return (NULL);
	}
	next = ft_calloc((ft_strlen(buffer) - i + 1), sizeof(char));
	i++;
	while (buffer[i])
		next[j++] = buffer[i++];
	free(buffer);
	return (next);
}

char	*ft_line(char *buffer)
{
	char	*line;
	int		i;

	i = 0;
	if (!buffer[i])
		return (NULL);
	while (buffer[i] && buffer[i] != '\n')
		i++;
	line = ft_calloc(i + 2, sizeof(char));
	if (!line)
		return (NULL);
	i = 0;
	while (buffer[i] && buffer[i] != '\n')
	{
		line[i] = buffer[i];
		i++;
	}
	if (buffer[i] && buffer[i] == '\n')
		line[i++] = '\n';
	return (line);
}

char	*read_the_file_bart(int fd, char *res)
{
	char	*buffer;
	int		num_bytes;

	if (!res)
		res = ft_calloc(1, 1);
	buffer = ft_calloc(BUFFER_SIZE + 1, sizeof(char));
	if (!buffer)
		return (NULL);
	num_bytes = 1;
	while (!ft_strchr(res, '\n') && num_bytes > 0)
	{
		num_bytes = read(fd, buffer, BUFFER_SIZE);
		if (num_bytes == -1)
		{
			free(buffer);
			free(res);
			return (NULL);
		}
		buffer[num_bytes] = 0;
		res = ft_free(res, buffer);
		if (ft_strchr(res, '\n'))
			break ;
	}
	free(buffer);
	return (res);
}

char	*get_next_line(int file)
{
	static char	*buffer;
	char		*line;

	if (file < 0 || BUFFER_SIZE <= 0)
	{
		if (buffer)
		{
			free(buffer);
			buffer = NULL;
		}
		return (NULL);
	}
	buffer = read_the_file_bart(file, buffer);
	if (!buffer)
	{
		buffer = NULL;
		return (NULL);
	}
	line = ft_line(buffer);
	buffer = ft_next(buffer);
	return (line);
}

/*int main(void)
{
    int     fd;
    char    *line;
    int	i;

    i = 42;

    fd = open("test.txt", O_RDONLY);
    if (fd < 0)
        return (1);

    line = get_next_line(fd);
    if (line)
    {
        printf("%s", line);
        free(line);
    }

    close(fd);
    return (0);
}*/
