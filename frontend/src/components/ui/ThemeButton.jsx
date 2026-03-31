import './ThemeButton.css';

export default function ThemeButton({ text, onClick }) {
  return (
    <button className='theme-btn' onClick={onClick}>{text}</button>
  );
}