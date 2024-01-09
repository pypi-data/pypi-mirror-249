from flask_apscheduler import APScheduler

from flask_chest import FlaskChest


class FlaskChestExporter:
    def __init__(self, chest: FlaskChest, interval_minutes: int = 5):
        self.app = chest.app
        self.interval_minutes = interval_minutes
        self.scheduler = APScheduler()
        self.scheduler.init_app(self.app)
        self.scheduler.start()

    def start_export_task(self):
        self.scheduler.add_job(
            id="export_data_job",
            func=self.export_data,
            trigger="interval",
            minutes=self.interval_minutes,
        )

    def export_data(self):
        raise NotImplementedError("This method should be implemented by subclass.")
