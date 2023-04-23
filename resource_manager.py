import boto3

session = boto3.Session()

def resource_exists(resource_type, resource_name):
    """Check if a resource of the specified type and name already exists."""
    pass

def create_resource(resource_type, resource_name, **kwargs):
    """Create a new resource of the specified type and name."""
    pass

def delete_resource(resource_type, resource_name):
    """Delete the resource of the specified type and name."""
    pass

def update_resource(resource_type, resource_name, **kwargs):
    """Update the properties of the specified resource."""
    pass
