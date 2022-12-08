DO $$
DECLARE
    genre_id   genres.id%TYPE;
    name_genre genres.name_genre%TYPE;

BEGIN
    genre_id := 1000000;
    name_genre := 'genre_';
    FOR counter IN 1..10
        LOOP
            INSERT INTO genres (id, name_genre)
             VALUES (counter + genre_id, name_genre || 100+counter);
        END LOOP;
END;
$$

SELECT * FROM genres;
