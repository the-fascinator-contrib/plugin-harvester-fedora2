from java.io import ByteArrayInputStream
from org.python.core.util import FileUtil, StringUtil
from xml.etree import ElementTree

def restoreProperty(props, key):
    copyKey = "copyOf_" + key 
    if props.containsKey(copyKey):
        copyValue = props.remove(copyKey).toString()
        props.setProperty(key, copyValue)
    else:
        props.remove(key)

# setup namespaces
ElementTree._namespace_map["http://www.loc.gov/MARC21/slim"] = "marc"
ElementTree._namespace_map["http://www.w3.org/2001/XMLSchema-instance"] = "xsi"

# parse the marc payload and reserialize with proper namespaces
props = object.getMetadata()
try:
    #sourcePayload = object.getPayload(object.getSourceId())
    sourcePayload = object.getPayload("DS1")
    tree = ElementTree.ElementTree()
    elem = tree.parse(FileUtil.wrap(sourcePayload.open()))
    xml = ElementTree.tostring(elem)
    sourcePayload.close()

    # save to new payload
    xmlBytes = ByteArrayInputStream(StringUtil.toBytes(xml))
    
    try:
        newPayloadId = "MARC"
        props.setProperty("modified", "true");
        #Can be processing multiple payload...
        props.setProperty("payloadToDelete.1", "DS1")
        props.setProperty("payloadToExport.1", "MARC")
        fixedPayload = object.createStoredPayload(newPayloadId, xmlBytes)
    except:
        print "Fail to create new payload, '%s' is already exist" % newPayloadId
        #revert back the properties as this object might be modified before but not exported yet
        restoreProperty(props, "indexOnHarvest")
        restoreProperty(props, "harvestQueue")
        restoreProperty(props, "renderQueue")
        restoreProperty(props, "jythonScript")
except:
    props.setProperty("modified", "false");

object.close()


