"""CLI commands for the application."""
import click
from faker import Faker
from app.models import db, Post


def register_commands(app):
    """Register CLI commands with the Flask app."""

    @app.cli.command('seed-db')
    @click.option('--count', default=50, help='Number of posts to create')
    def seed_database(count):
        """Seed the database with sample data."""
        click.echo(f'Creating {count} sample posts...')

        fake = Faker()
        posts = []

        for _ in range(count):
            post = Post(
                title=fake.sentence(nb_words=6)[:-1],  # Remove trailing period
                content=fake.text(max_nb_chars=500)
            )
            posts.append(post)

        db.session.bulk_save_objects(posts)
        db.session.commit()

        click.echo(f'Successfully created {count} posts!')

    @app.cli.command('clear-db')
    @click.confirmation_option(prompt='Are you sure you want to delete all posts?')
    def clear_database():
        """Clear all posts from the database."""
        count = Post.query.count()
        Post.query.delete()
        db.session.commit()
        click.echo(f'Deleted {count} posts from the database.')

    @app.cli.command('db-stats')
    def database_stats():
        """Display database statistics."""
        post_count = Post.query.count()

        click.echo('Database Statistics:')
        click.echo(f'  Total Posts: {post_count}')

        if post_count > 0:
            latest_post = Post.query.order_by(Post.created_at.desc()).first()
            oldest_post = Post.query.order_by(Post.created_at.asc()).first()

            click.echo(f'  Latest Post: {latest_post.title} ({latest_post.created_at})')
            click.echo(f'  Oldest Post: {oldest_post.title} ({oldest_post.created_at})')

    @app.cli.command('create-admin')
    @click.option('--username', prompt='Username', help='Admin username')
    @click.option('--email', prompt='Email', help='Admin email')
    def create_admin(username, email):
        """Create an admin user (placeholder for future auth system)."""
        click.echo(f'Creating admin user: {username} ({email})')
        click.echo('Note: User authentication is not yet implemented.')
        click.echo('This is a placeholder for future functionality.')

    @app.cli.command('export-posts')
    @click.option('--format', type=click.Choice(['json', 'csv']), default='json')
    @click.option('--output', default='posts_export', help='Output filename (without extension)')
    def export_posts(format, output):
        """Export all posts to JSON or CSV."""
        import json
        import csv
        from datetime import datetime

        posts = Post.query.all()

        if format == 'json':
            filename = f'{output}.json'
            data = [post.to_dict() for post in posts]

            with open(filename, 'w') as f:
                json.dump(data, f, indent=2, default=str)

            click.echo(f'Exported {len(posts)} posts to {filename}')

        elif format == 'csv':
            filename = f'{output}.csv'

            with open(filename, 'w', newline='') as f:
                if posts:
                    fieldnames = ['id', 'title', 'content', 'created_at', 'updated_at']
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()

                    for post in posts:
                        writer.writerow(post.to_dict())

            click.echo(f'Exported {len(posts)} posts to {filename}')

    @app.cli.command('backup-db')
    def backup_database():
        """Create a backup of the database."""
        import shutil
        from datetime import datetime

        # This is for SQLite - adjust for other databases
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = f'backup_{timestamp}_{db_path}'

        try:
            shutil.copy2(db_path, backup_path)
            click.echo(f'Database backed up to: {backup_path}')
        except FileNotFoundError:
            click.echo('Error: Database file not found. Run the app first to create it.')
        except Exception as e:
            click.echo(f'Error creating backup: {str(e)}')
