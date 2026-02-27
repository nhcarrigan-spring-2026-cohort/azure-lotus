from sqlmodel import Session, select


from src.core.auth.security import hash_password
from src.core.database.session import engine
from src.features.alerts.models import Alert
from src.features.checkins.models import CheckIn
from src.features.relationships.models import Relationship
from src.features.users.models import User

def get_or_create_user(
	session: Session,
	first_name: str,
	last_name: str,
	email: str,
	phone_number: str,
	raw_password: str,
) -> User:
	# Look up by unique email so rerunning seed won't create duplicates.
	existing_user = session.exec(select(User).where(User.email == email)).first()
	if existing_user:
		return existing_user

	# Create baseline user only when it does not already exist.
	user = User(
		first_name=first_name,
		last_name=last_name,
		email=email,
		phone_number=phone_number,
		hashed_password=hash_password(raw_password),
	)
	# Flush to persist and make the generated UUID available immediately.
	session.add(user)
	session.flush()
	return user


def get_or_create_relationship(
	session: Session,
	senior_id,
	caregiver_id,
	priority: int = 1,
) -> Relationship:
	# Relationship is unique for a senior/caregiver pair in this seed setup.
	existing_relationship = session.exec(
		select(Relationship).where(
			Relationship.senior_id == senior_id,
			Relationship.caregiver_id == caregiver_id,
		)
	).first()
	if existing_relationship:
		return existing_relationship

	# Create baseline relationship only if one doesn't already exist.
	relationship = Relationship(
		senior_id=senior_id,
		caregiver_id=caregiver_id,
		priority=priority,
	)
	# Flush so downstream records can reference relationship.id.
	session.add(relationship)
	session.flush()
	return relationship


def get_or_create_checkin(session: Session, relationship_id) -> CheckIn:
	# Keep one seed check-in per relationship.
	existing_checkin = session.exec(
		select(CheckIn).where(CheckIn.relationship_id == relationship_id)
	).first()
	if existing_checkin:
		return existing_checkin

	# Create a pending check-in baseline row.
	checkin = CheckIn(
		relationship_id=relationship_id,
		status="pending",
	)
	# Flush so alert creation can reference checkin.id.
	session.add(checkin)
	session.flush()
	return checkin


def get_or_create_alert(session: Session, checkin_id, alert_type: str = "missed_checkin") -> Alert:
	# Prevent duplicate alerts for the same checkin + alert type.
	existing_alert = session.exec(
		select(Alert).where(
			Alert.checkin_id == checkin_id,
			Alert.alert_type == alert_type,
		)
	).first()
	if existing_alert:
		return existing_alert

	# Create baseline alert row for demo/initial workflow.
	alert = Alert(
		checkin_id=checkin_id,
		alert_type=alert_type,
		resolved=False,
	)
	# Flush to keep write order explicit before commit.
	session.add(alert)
	session.flush()
	return alert


def seed_database() -> None:
	# Use a single transaction so baseline data is all-or-nothing.
	with Session(engine) as session:
		try:
			# Seed one caregiver user.
			caregiver = get_or_create_user(
				session=session,
				first_name="Alice",
				last_name="Caregiver",
				email="alice.caregiver@example.com",
				phone_number="+15550000001",
				raw_password="Password123",
			)

			# Seed one senior user.
			senior = get_or_create_user(
				session=session,
				first_name="Sam",
				last_name="Senior",
				email="sam.senior@example.com",
				phone_number="+15550000002",
				raw_password="Password123",
			)

			# Link caregiver and senior.
			relationship = get_or_create_relationship(
				session=session,
				senior_id=senior.id,
				caregiver_id=caregiver.id,
				priority=1,
			)

			# Create a check-in baseline row for that relationship.
			checkin = get_or_create_checkin(
				session=session,
				relationship_id=relationship.id,
			)

			# Create a baseline alert tied to the check-in.
			get_or_create_alert(
				session=session,
				checkin_id=checkin.id,
				alert_type="missed_checkin",
			)

			# Persist all inserts/updates once at the end.
			session.commit()
			print("Seed complete: baseline users, relationship, checkin, and alert are ready.")
		except Exception:
			# Roll back everything if any seed step fails.
			session.rollback()
			raise


if __name__ == "__main__":
	seed_database()
