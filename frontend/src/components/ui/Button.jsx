import './Button.css';

export default function Button({
  children,
  variant = 'primary',
  size = 'medium',
  className = '',
  ...props
}) {
  const buttonClass = `btn btn-${variant} btn-${size} ${className}`;

  return (
    
    <button className={buttonClass} {...props}>
      {children}
    </button>
  );
}
