import * as React from 'react';

export interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  fullWidth?: boolean;
  onClick?: () => void;
  type?: 'button' | 'submit' | 'reset';
}

const VARIANT_STYLES = {
  primary: {
    backgroundColor: '#3b82f6',
    color: '#ffffff',
    border: 'none',
  },
  secondary: {
    backgroundColor: '#f3f4f6',
    color: '#1f2937',
    border: '1px solid #d1d5db',
  },
  ghost: {
    backgroundColor: 'transparent',
    color: '#3b82f6',
    border: 'none',
  },
  danger: {
    backgroundColor: '#ef4444',
    color: '#ffffff',
    border: 'none',
  },
} as const;

const SIZE_STYLES = {
  sm: {
    padding: '6px 12px',
    fontSize: '14px',
    borderRadius: '4px',
  },
  md: {
    padding: '8px 16px',
    fontSize: '16px',
    borderRadius: '6px',
  },
  lg: {
    padding: '12px 24px',
    fontSize: '18px',
    borderRadius: '8px',
  },
} as const;

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      children,
      variant = 'primary',
      size = 'md',
      disabled = false,
      loading = false,
      fullWidth = false,
      onClick,
      type = 'button',
    },
    ref
  ) => {
    const baseStyles: React.CSSProperties = {
      display: 'inline-flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontWeight: 500,
      cursor: disabled || loading ? 'not-allowed' : 'pointer',
      opacity: disabled ? 0.5 : 1,
      transition: 'all 150ms ease',
      width: fullWidth ? '100%' : 'auto',
      gap: '8px',
    };

    const combinedStyles: React.CSSProperties = {
      ...baseStyles,
      ...VARIANT_STYLES[variant],
      ...SIZE_STYLES[size],
    };

    return (
      <button
        ref={ref}
        type={type}
        disabled={disabled || loading}
        onClick={onClick}
        style={combinedStyles}
        onMouseEnter={(e) => {
          if (!disabled && !loading) {
            e.currentTarget.style.opacity = '0.9';
            e.currentTarget.style.transform = 'translateY(-1px)';
          }
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.opacity = disabled ? '0.5' : '1';
          e.currentTarget.style.transform = 'translateY(0)';
        }}
      >
        {loading && (
          <span
            style={{
              width: '16px',
              height: '16px',
              border: '2px solid currentColor',
              borderTopColor: 'transparent',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
            }}
          />
        )}
        {children}
      </button>
    );
  }
);

Button.displayName = 'Button';
