import logging
import pytest
from CommonUtilities.utilities import file_to_db_verify, db_to_db_verify
from Config.config import *
from TestScripts.conftest import ExecutionFlow, Sales_Data_From_Linux_Server


# Logging mechanism
logging.basicConfig(
    filename='Logs/etlprocess.log',  # Name of the log file
    filemode='a',  # 'a' to append, 'w' to overwrite
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log format
    level=logging.INFO  # Set the logging level
)
logger = logging.getLogger(__name__)

@pytest.mark.usefixtures("ExecutionFlow")
class TestDataExtractionTestCases:

    # Data extraction from Sales Data (Linux Server)
    @pytest.mark.Linux_souces
    @pytest.mark.skip  # Marking this test as skipped for now
    def test_extraction_from_sales_data_CSV_to_sales_staging_MySQL(self, mysql_engine, Sales_Data_From_Linux_Server):
        logger.info("Data extraction from sales_data.csv to sales_staging has started .......")
        try:
            file_to_db_verify('Testdata/sales_data_Linux.csv', 'csv', 'staging_sales', mysql_engine)
            logger.info("Data extraction from sales_data.csv to sales_staging has completed .......")
        except Exception as e:
            logger.error(f"Error occurred during data extraction: {e}")
            pytest.fail(f"Test failed due to an error {e}")

    # Data extraction from Product Data (CSV to MySQL)
    @pytest.mark.smoke
    def test_extraction_from_product_data_CSV_to_product_staging_MySQL(self, mysql_engine, ExecutionFlow):
        logger.info("Data extraction from product_data.csv to product_staging has started .......")
        try:
            file_to_db_verify('Testdata/product_data.csv', 'csv', 'staging_product', mysql_engine)
            logger.info("Data extraction from product_data.csv to product_staging has completed .......")
        except Exception as e:
            logger.error(f"Error occurred during data extraction: {e}")
            pytest.fail(f"Test failed due to an error {e}")

    # Data extraction from Supplier Data (JSON to MySQL)
    @pytest.mark.regression
    def test_extraction_from_supplier_data_JSON_to_supplier_staging_MySQL(self, mysql_engine, ExecutionFlow):
        logger.info("Data extraction from supplier_data.json to supplier_staging has started .......")
        try:
            file_to_db_verify('Testdata/supplier_data.json', 'json', 'staging_supplier', mysql_engine)
            logger.info("Data extraction from supplier_data.json to supplier_staging has completed .......")
        except Exception as e:
            logger.error(f"Error occurred during data extraction: {e}")
            pytest.fail(f"Test failed due to an error {e}")

    # Data extraction from Inventory Data (XML to MySQL)
    @pytest.mark.regression
    def test_extraction_from_inventory_data_XML_to_inventory_staging_MySQL(self, mysql_engine, ExecutionFlow):
        logger.info("Data extraction from inventory_data.xml to inventory_staging has started .......")
        try:
            file_to_db_verify('Testdata/inventory_data.xml', 'xml', 'staging_inventory', mysql_engine)
            logger.info("Data extraction from inventory_data.xml to inventory_staging has completed .......")
        except Exception as e:
            logger.error(f"Error occurred during data extraction: {e}")
            pytest.fail(f"Test failed due to an error {e}")

    # Data comparison between Oracle and MySQL for Store Table
    @pytest.mark.regression
    def test_extraction_from_store_ORCL_to_store_staging_MySQL(self, mysql_engine, oracle_engine, ExecutionFlow):
        logger.info("Data comparison from store table from Oracle to store_staging has started .......")
        try:
            query1 = """select * from stores"""
            query2 = """select * from staging_stores"""
            db_to_db_verify(query1, oracle_engine, query2, mysql_engine)
            logger.info("Data comparison from store table from Oracle to store_staging has completed .......")
        except Exception as e:
            logger.error(f"Error occurred during data extraction: {e}")
            pytest.fail(f"Test failed due to an error {e}")