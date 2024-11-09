from neomodel import StructuredNode, StringProperty, FloatProperty, IntegerProperty, RelationshipTo

class Stop(StructuredNode):
    stop_id = StringProperty(required=True, unique_index=True)
    name = StringProperty(required=True)
    wl_number = IntegerProperty()
    stop_latitude = FloatProperty(required=True)
    stop_longitude = FloatProperty(required=True)

    has_line = RelationshipTo('Line', 'HAS_LINE')

class School(StructuredNode):
    school_id = StringProperty(required=True, unique_index=True)
    address = StringProperty(required=True)
    type = StringProperty(required=True)
    type_text = StringProperty()
    care = StringProperty()
    phone = StringProperty()
    website = StringProperty()
    location_latitude = FloatProperty(required=True)
    location_longitude = FloatProperty(required=True)
    name = StringProperty(required=True)
    rating = IntegerProperty()
    
    is_nearby = RelationshipTo('Stop', 'IS_NEARBY')
    is_in_area = RelationshipTo('Stop', 'IS_IN_AREA')


class Line(StructuredNode):
    name = StringProperty(required=True)
    type = StringProperty()
