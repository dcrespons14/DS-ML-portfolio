# Portfolio search

## Database documentation

The Project Search application logs user queries to a PostgreSQL database hosted on Supabase.  
This is used to gather feedback on how users interact with the search functionality.

### Table: `project_search_queries`

The table contains the following columns:

- `id` — `int8`, primary key.
- `time_stamp` — `timestamptz`, automatically set to the current time when the query is inserted.
- `query` — `text`, the search query entered by the user.

### Security

Row Level Security (RLS) is enabled on this table to control access.

A policy is configured to allow `INSERT` operations for clients using the Supabase **publishable key**.  
This enables the application to log user queries while preventing unrestricted access to the table contents.

Furthermore, both `url` and `key` are securely stored as environment variables in `Render` using the secrets functionality.
