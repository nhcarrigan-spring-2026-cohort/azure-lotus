import useTitle from "../components/hooks/useTitle";
import FamilyRegistrationForm from "../components/ui/FamilyRegistrationForm";

export default function signup() {
  useTitle("Sign Up");
  return (
    <>
      <FamilyRegistrationForm />
    </>
  );
}
