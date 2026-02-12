import './Input.css';

export default function Input({
  id,
  name,
  type = 'text',
  placeholder,
  value,
  onChange,
  error = '',
  className = '',
  ...rest
}) {
  return (
    <div className="input-container">
      <input
        id={id}
        name={name}
        type={type}
        placeholder={placeholder}
        value={value}
        onChange={onChange}
        className={`input-field ${error ? 'errored' : ''} ${className}`}
        {...rest}
      />
      {error && <span className="error-text">{error}</span>}
    </div>
  );
}
