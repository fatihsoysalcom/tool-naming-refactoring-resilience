class StorageTool:
    """Represents a generic storage tool."""
    def __init__(self, name):
        self.name = name

    def store(self, data):
        raise NotImplementedError("Subclasses must implement 'store' method.")

class AWSS3Storage(StorageTool):
    def __init__(self):
        super().__init__("AWS S3 Storage")
    
    def store(self, data):
        print(f"[{self.name}] Storing '{data}' in an S3 bucket.")

class AzureBlobStorage(StorageTool):
    def __init__(self):
        super().__init__("Azure Blob Storage")

    def store(self, data):
        print(f"[{self.name}] Storing '{data}' in an Azure blob container.")

class GoogleCloudStorage(StorageTool):
    def __init__(self):
        super().__init__("Google Cloud Storage")

    def store(self, data):
        print(f"[{self.name}] Storing '{data}' in a GCS bucket.")

# --- Naming Pattern 1: Technology-Specific Naming (Less Resilient) ---
# Client code directly references the specific technology tool.

def process_user_data_v1(data):
    """
    Processes user data using a directly referenced AWS S3 tool.
    This naming is specific to AWS S3.
    """
    print("\n--- Pattern 1: Technology-Specific Naming ---")
    aws_s3_tool = AWSS3Storage() # Direct instantiation/reference, tightly coupled
    aws_s3_tool.store(data)
    print("Client code is tightly coupled to 'AWSS3Storage'.")

# --- Naming Pattern 2: Purpose-Driven/Abstract Naming (More Resilient) ---
# Client code references a tool by its purpose, and the actual implementation
# is resolved via a configuration or a service locator.

# A simple "service locator" or "tool registry"
_tool_registry = {}

def register_tool(purpose_name, tool_instance):
    """Registers a tool instance under a given purpose-driven name."""
    _tool_registry[purpose_name] = tool_instance

def get_tool(purpose_name):
    """Retrieves a tool instance by its purpose-driven name."""
    tool = _tool_registry.get(purpose_name)
    if not tool:
        raise ValueError(f"Tool for purpose '{purpose_name}' not registered.")
    return tool

# Initial setup: Register a tool for 'user_profile_storage' purpose
register_tool("user_profile_storage", AWSS3Storage()) # Initially points to AWS S3

def process_user_data_v2(data):
    """
    Processes user data using a purpose-driven 'user_profile_storage' tool.
    This naming is abstract and resilient to underlying technology changes.
    """
    print("\n--- Pattern 2: Purpose-Driven/Abstract Naming ---")
    # Client code uses the abstract name 'user_profile_storage'
    user_storage_tool = get_tool("user_profile_storage") 
    user_storage_tool.store(data)
    print("Client code is coupled to 'user_profile_storage' purpose, not specific tech.")

# --- Demonstration of Refactoring Resilience ---

if __name__ == "__main__":
    # Initial state
    process_user_data_v1("Alice's profile data")
    process_user_data_v2("Bob's profile data")

    # --- Simulating Refactoring for Pattern 1 (Manual Change Required) ---
    # To change storage for Pattern 1, one would need to manually find and replace
    # 'AWSS3Storage()' with 'AzureBlobStorage()' everywhere it's used in client code.
    print("\n--- Simulating Refactoring for Pattern 1 (Low Resilience) ---")
    print("If 'process_user_data_v1' needed to switch to Azure, its internal code")
    print("would have to be manually changed from 'AWSS3Storage()' to 'AzureBlobStorage()'.")
    print("This demonstrates low refactoring resilience as client code needs modification.")

    # --- Simulating Refactoring for Pattern 2 (High Resilience) ---
    # We can change the underlying storage for 'user_profile_storage'
    # without modifying 'process_user_data_v2'.
    print("\n--- Simulating Refactoring for Pattern 2 (High Resilience) ---")
    print("Refactoring: Switching 'user_profile_storage' from AWS S3 to Azure Blob Storage.")
    register_tool("user_profile_storage", AzureBlobStorage()) # Only change here in the registry!

    print("\nAfter refactoring:")
    process_user_data_v2("Charlie's profile data") # No change needed in this client code
    print("Client code ('process_user_data_v2') remained unchanged.")
    print("This demonstrates high refactoring resilience due to abstract naming.")

    # Another refactoring: Switch to Google Cloud Storage
    print("\nRefactoring: Switching 'user_profile_storage' from Azure to Google Cloud Storage.")
    register_tool("user_profile_storage", GoogleCloudStorage()) # Only change here!

    print("\nAfter second refactoring:")
    process_user_data_v2("David's profile data") # Still no change needed in client code
    print("Client code ('process_user_data_v2') still remained unchanged.")
    print("This further demonstrates high refactoring resilience.")
