from django.test import TestCase
from connectly_project.singletons.logger_singleton import LoggerSingleton

class LoggerSingletonTest(TestCase):
    def test_singleton_logger(self):
        """Test that LoggerSingleton maintains a single instance"""
        
        logger1 = LoggerSingleton().get_logger()
        logger2 = LoggerSingleton().get_logger()

        self.assertIs(logger1, logger2)

        
        with self.assertLogs(logger1, level="INFO") as log_output:
            logger1.info("Testing Singleton Logger")

        self.assertIn("INFO:connectly_logger:Testing Singleton Logger", log_output.output)
