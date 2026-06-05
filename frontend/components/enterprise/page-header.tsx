interface PageHeaderProps {
  title: string;
  description?: string;
  badge?: string;
  children?: React.ReactNode;
}

export function PageHeader({
  title,
  description,
  badge,
  children,
}: PageHeaderProps) {
  return (
    <div className="mb-8 flex flex-col gap-4 border-b border-white/[0.06] pb-6 lg:flex-row lg:items-end lg:justify-between">
      <div>
        {badge && (
          <span className="mb-2 inline-block rounded-md border border-blue-500/20 bg-blue-500/10 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-widest text-blue-400">
            {badge}
          </span>
        )}
        <h1 className="text-2xl font-semibold tracking-tight lg:text-3xl">
          {title}
        </h1>
        {description && (
          <p className="mt-1.5 max-w-2xl text-sm text-muted-foreground">
            {description}
          </p>
        )}
      </div>
      {children && <div className="flex items-center gap-2">{children}</div>}
    </div>
  );
}
