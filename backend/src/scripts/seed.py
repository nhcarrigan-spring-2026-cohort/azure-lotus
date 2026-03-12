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


def get_or_create_checkin(session: Session, senior_id) -> CheckIn:
	# Keep one seed check-in per relationship.
	existing_checkin = session.exec(
		select(CheckIn).where(CheckIn.senior_id == senior_id)
	).first()
	if existing_checkin:
		return existing_checkin	
	
	# Create a pending check-in baseline row.
	checkin = CheckIn(
		senior_id=senior_id,
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
	with Session(engine) as session:
		try:
			# -------------------------
			# CAREGIVERS
			# -------------------------
			caregivers_data = [
				("Alice", "Caregiver", "alice.caregiver@example.com", "+15550000001"),
				("Bob", "Helper", "bob.helper@example.com", "+15550000003"),
				("Carol", "Support", "carol.support@example.com", "+15550000004"),
			]

			caregivers = []
			for first_name, last_name, email, phone in caregivers_data:
				user = get_or_create_user(
					session=session,
					first_name=first_name,
					last_name=last_name,
					email=email,
					phone_number=phone,
					raw_password="Password123",
				)
				caregivers.append(user)

			# -------------------------
			# SENIORS
			# -------------------------
			seniors_data = [
				("Sam", "Senior", "sam.senior@example.com", "+15550000002"),
				("Doris", "Elder", "doris.elder@example.com", "+15550000005"),
				("Frank", "Golden", "frank.golden@example.com", "+15550000006"),
			]

			seniors = []
			for first_name, last_name, email, phone in seniors_data:
				user = get_or_create_user(
					session=session,
					first_name=first_name,
					last_name=last_name,
					email=email,
					phone_number=phone,
					raw_password="Password123",
				)
				seniors.append(user)

			# -------------------------
			# RELATIONSHIPS
			# -------------------------
			relationships = []
			for i, senior in enumerate(seniors):
				for priority, caregiver in enumerate(caregivers, start=1):
					relationship = get_or_create_relationship(
						session=session,
						senior_id=senior.id,
						caregiver_id=caregiver.id,
						priority=priority,
					)
					relationships.append(relationship)

			# -------------------------
			# CHECKINS + ALERTS
			# -------------------------
			for senior in seniors:
				# Pending check-in
				checkin_pending = get_or_create_checkin(
					session=session,
					senior_id=senior.id,
				)

				get_or_create_alert(
					session=session,
					checkin_id=checkin_pending.id,
					alert_type="missed_checkin",
				)

				# Extra manual check-in example (não usa helper para permitir múltiplos)
				extra_checkin = CheckIn(
					senior_id=senior.id,
					status="completed",
				)
				session.add(extra_checkin)
				session.flush()

				get_or_create_alert(
					session=session,
					checkin_id=extra_checkin.id,
					alert_type="manual_review",
				)

			session.commit()
			print("Seed complete: multiple caregivers, seniors, relationships, checkins and alerts created.")
		except Exception:
			session.rollback()
			raise


if __name__ == "__main__":
	seed_database()
