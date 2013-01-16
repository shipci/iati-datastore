from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,DateTime,Date,BigInteger,Float,ForeignKey,Boolean,UnicodeText
from . import engine

Base = declarative_base()

class IndexedResource(Base):
    __tablename__ = 'indexed_resource'
    id = Column(UnicodeText, primary_key=True)
    url = Column(UnicodeText)
    last_modified = Column(DateTime)
    state = Column(Integer)

class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    parent_resource = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    # TODO remove
    package_id = Column(UnicodeText)
    # TODO remove
    source_file = Column(UnicodeText)
    activity_lang = Column(UnicodeText)
    default_currency = Column(UnicodeText)
    hierarchy = Column(UnicodeText)
    last_updated = Column(UnicodeText)
    reporting_org = Column(UnicodeText)
    reporting_org_ref = Column(UnicodeText)
    reporting_org_type = Column(UnicodeText)
    funding_org = Column(UnicodeText)
    funding_org_ref = Column(UnicodeText)
    funding_org_type = Column(UnicodeText)
    extending_org = Column(UnicodeText)
    extending_org_ref = Column(UnicodeText)
    extending_org_type = Column(UnicodeText)
    implementing_org = Column(UnicodeText)
    implementing_org_ref = Column(UnicodeText)
    implementing_org_type = Column(UnicodeText)
    recipient_region = Column(UnicodeText)
    recipient_region_code = Column(UnicodeText)
    recipient_country = Column(UnicodeText)
    recipient_country_code = Column(UnicodeText)
    collaboration_type = Column(UnicodeText)
    collaboration_type_code = Column(UnicodeText)
    flow_type = Column(UnicodeText)
    flow_type_code = Column(UnicodeText)
    aid_type = Column(UnicodeText)
    aid_type_code = Column(UnicodeText)
    finance_type = Column(UnicodeText)
    finance_type_code = Column(UnicodeText)
    iati_identifier = Column(UnicodeText, index=True)
    title = Column(UnicodeText)
    description = Column(UnicodeText)
    date_start_actual = Column(UnicodeText)
    date_start_planned = Column(UnicodeText)
    date_end_actual = Column(UnicodeText)
    date_end_planned = Column(UnicodeText)
    status_code = Column(UnicodeText)
    status = Column(UnicodeText)
    contact_organisation = Column(UnicodeText)
    contact_telephone = Column(UnicodeText)
    contact_email = Column(UnicodeText)
    contact_mailing_address = Column(UnicodeText)
    tied_status = Column(UnicodeText)
    tied_status_code = Column(UnicodeText)
    activity_website = Column(UnicodeText)

class Transaction(Base):
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    parent_resource = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    activity_id = Column(UnicodeText)
    value = Column(Float)
    iati_identifier = Column(UnicodeText, index=True)
    value_date = Column(UnicodeText)
    value_currency = Column(UnicodeText)
    transaction_type = Column(UnicodeText)
    transaction_type_code = Column(UnicodeText)
    provider_org = Column(UnicodeText)
    provider_org_ref = Column(UnicodeText)
    provider_org_type = Column(UnicodeText)
    receiver_org = Column(UnicodeText)
    receiver_org_ref = Column(UnicodeText)
    receiver_org_type = Column(UnicodeText)
    description = Column(UnicodeText)
    transaction_date = Column(UnicodeText)
    transaction_date_iso = Column(UnicodeText)
    flow_type = Column(UnicodeText)
    flow_type_code = Column(UnicodeText)
    aid_type = Column(UnicodeText)
    aid_type_code = Column(UnicodeText)
    finance_type = Column(UnicodeText)
    finance_type_code = Column(UnicodeText)
    tied_status = Column(UnicodeText)
    tied_status_code = Column(UnicodeText)
    disbursement_channel_code = Column(UnicodeText)

# Put everything into sectors table, and link back to activity. This will create a new unique sector per activity, which is OK for then importing back into OS but obviously you would probably want an activities_sectors table to handle a relationship between unique activities and unique sectors.
 
class Sector(Base):
    __tablename__ = 'sector'
    id = Column(Integer, primary_key=True)   
    parent_resource = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    activity_iati_identifier = Column(UnicodeText, index=True)
    name = Column(UnicodeText)
    vocabulary = Column(UnicodeText)
    code = Column(UnicodeText)
    percentage = Column(Integer)

class RelatedActivity(Base):
    __tablename__ = 'relatedactivity'
    id = Column(Integer, primary_key=True)
    parent_resource = Column(UnicodeText, ForeignKey('indexed_resource.id'), nullable=False)
    activity_id = Column(UnicodeText, index=True)
    reltext = Column(UnicodeText)
    relref = Column(UnicodeText)
    reltype = Column(UnicodeText)
