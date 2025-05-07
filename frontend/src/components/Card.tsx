// src/components/Card.tsx
import { PropsWithChildren, ReactNode } from "react";

interface CardProps extends PropsWithChildren {
  title: string;
  icon?: ReactNode;
}

export default function Card({ title, icon, children }: CardProps) {
  return (
    <div
      className={`
        relative flex flex-col gap-4 rounded-4xl
        bg-white/10 border border-white/20
        p-6
        shadow-[0_4px_30px_rgba(0,0,0,0.1)]
        backdrop-blur-xl
        transition
        hover:bg-white/20 hover:shadow-[0_8px_40px_rgba(0,0,0,0.2)]
      `}
    >
      <header className="flex items-center gap-2">
        {icon && <span className="text-white text-xl">{icon}</span>}
        <h3 className="text-white/90 font-semibold text-lg">{title}</h3>
      </header>

      <div className="flex-1">
        {children ?? (
          <p className="text-white/50 text-sm">Contenu à venir…</p>
        )}
      </div>
    </div>
  );
}

