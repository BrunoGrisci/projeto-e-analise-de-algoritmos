# Projeto e Análise de Algoritmos I
# Distância em grafos valorados.
# Bruno Iochins Grisci e Rodrigo Machado
# Universidade Federal do Rio Grande do Sul
# Instituto de Informática
# Departamento de Informática Teórica


#!/usr/bin/env python3
"""
Interactive Min-Heap demo with colored tracing (blue highlights).

- Use `verbose on` to see colored swap/insert tracing.
- Works without external deps; if `colorama` is installed, it initializes on Windows.

Example:
  minheap> load [7,3,10,9,4,12,8,15,20,5]
  minheap> verbose on
  minheap> push 2
  minheap> pop
"""

from typing import List, Iterable, Optional, Any, Sequence, Set
import ast, random, sys, os

# --- Color helpers -----------------------------------------------------------

BLUE = BOLD = RESET = DIM = ""
def _init_colors():
    global BLUE, BOLD, RESET, DIM
    supports = sys.stdout.isatty()
    # Try to enable ANSI on Windows via colorama if available
    if os.name == "nt":
        try:
            import colorama
            colorama.just_fix_windows_console()
            supports = True
        except Exception:
            pass
    if supports:
        # Robust ANSI constants (with ESC prefix)
        ESC   = "\x1b["                 # use \x1b instead of \033 to avoid copy/paste issues
        RESET = ESC + "0m"
        BOLD  = ESC + "1m"
        BLUE  = ESC + "36m"             # or "36m" if you want cyan
_init_colors()

def blue(s: str) -> str:
    return f"{BLUE}{s}{RESET}" if BLUE else s

def bold(s: str) -> str:
    return f"{BOLD}{s}{RESET}" if BOLD else s

def wait_for_enter(prompt="Press Enter to continue..."):
    """Pause until user presses Enter, if verbose mode is on."""
    try:
        input(prompt)
    except EOFError:
        pass
    print("\n\n")

# --------------------------- Min-Heap (didactic) -----------------------------

class MinHeap:
    """0-based array min-heap with visualizations and colored tracing."""

    def __init__(self, data: Optional[Iterable[Any]] = None, verbose: bool = False):
        self.A: List[Any] = list(data) if data is not None else []
        self.verbose = verbose
        self._heapify()

    # Public API
    def push(self, x: Any) -> None:
        self.A.append(x)
        i = len(self.A) - 1
        if self.verbose:
            print(f"{bold('[push]')} inserted {blue(repr(x))} at index {blue(str(i))}")
            self.visualize("  state (after append)", highlights={i})
            wait_for_enter()
        self._sift_up(i)

    def pop(self) -> Any:
        if not self.A:
            raise IndexError("pop from empty heap")
        if self.verbose:
            print(bold("[pop] remove min at root"))
            wait_for_enter()
        last = len(self.A) - 1
        self._swap(0, last, reason="root <-> last before removal")
        m = self.A.pop()
        if self.A:
            self._sift_down(0)
        return m

    def peek(self) -> Any:
        if not self.A:
            raise IndexError("peek from empty heap")
        return self.A[0]

    def clear(self) -> None:
        self.A.clear()

    def heapify_from(self, data: Iterable[Any]) -> None:
        self.A = list(data)
        if self.verbose:
            print(bold("[heapify] starting from array: "), self.A)
            wait_for_enter()
        self._heapify()
        if self.verbose:
            self.visualize("  state (after heapify)")
            wait_for_enter()

    def __len__(self) -> int:
        return len(self.A)

    # Internals
    def _heapify(self) -> None:
        for i in range((len(self.A) - 2) // 2, -1, -1):
            self._sift_down(i)

    def _sift_up(self, i: int) -> None:
        """Bubble A[i] up until heap property is restored."""
        moved = False
        start_i = i
        while i > 0:
            p = (i - 1) // 2
            if self.A[p] <= self.A[i]:
                # No violation; stop
                break
            moved = True
            self._swap(p, i, reason="sift-up")
            i = p
        if self.verbose and not moved:
            print(f"  [check] sift-up at index {start_i} (no change)")
            wait_for_enter()


    def _sift_down(self, i: int) -> None:
        n = len(self.A)
        moved = False
        start_i = i
        while True:
            l = 2*i + 1
            r = 2*i + 2
            s = i
            if l < n and self.A[l] < self.A[s]: s = l
            if r < n and self.A[r] < self.A[s]: s = r
            if s == i:
                if self.verbose and not moved:
                    print(f"  [check] sift-down at index {start_i} (no change)")
                    wait_for_enter()
                break
            moved = True
            self._swap(i, s, reason="sift-down")
            i = s


    def _swap(self, i: int, j: int, *, reason: str = "swap") -> None:
        ai, aj = self.A[i], self.A[j]
        self.A[i], self.A[j] = aj, ai
        if self.verbose:
            msg = (f"  {bold('[swap]')} {reason}: "
                   f"index {blue(str(i))} ({blue(repr(ai))}) "
                   f"<-> index {blue(str(j))} ({blue(repr(aj))})")
            print(msg)
            self.visualize("  state", highlights={i, j})
            wait_for_enter()

    def delete_at(self, i: int) -> Any:
        """
        Delete and return the element at array index i in O(log n).
        Strategy: swap(i, last), pop last, then sift up or down from i.
        """
        n = len(self.A)
        if i < 0 or i >= n:
            raise IndexError(f"delete_at: index out of range ({i})")

        if self.verbose:
            val = self.A[i]
            print(f"{BOLD}[delete]{RESET} remove index {BLUE}{i}{RESET} value {BLUE}{val!r}{RESET}")
            wait_for_enter()

        last = n - 1
        if i == last:
            # Just remove the last one
            removed = self.A.pop()
            if self.verbose:
                self.visualize("  state (after delete)")
                wait_for_enter()
            return removed

        # Move the last element into position i, remove original value
        self._swap(i, last, reason="delete: swap with last")
        removed = self.A.pop()

        # Fix heap from i: decide direction by comparing with parent
        if i > 0 and self.A[i] < self.A[(i - 1) // 2]:
            self._sift_up(i)
        else:
            self._sift_down(i)

        if self.verbose:
            self.visualize("  state (after delete)")
            wait_for_enter()
        return removed


    # Visualization
    def visualize(self, label: str = "", highlights: Optional[Set[int]] = None) -> None:
        if label:
            print(label)
        print("Array:", self._format_array(highlights or set()))
        print(self._ascii_tree(highlights or set()))
        print("\n")

    def _format_array(self, highlights: Set[int]) -> str:
        out = []
        for idx, val in enumerate(self.A):
            text = f"{idx}:{val}"
            if idx in highlights:
                text = f"{BOLD}{BLUE}{text}{RESET}"
            out.append(text)
        return "[" + ", ".join(out) + "]"

    def _ascii_tree(self, highlights: Set[int]) -> str:
        n = len(self.A)
        if n == 0:
            return "(empty)"

        # Build levels of array indices
        levels: List[List[int]] = []
        i = 0
        while i < n:
            width = 1 << len(levels)
            levels.append(list(range(i, min(i + width, n))))
            i += width

        # Node text is "i:v"
        labels = [f"{i}:{self.A[i]}" for i in range(n)]
        cellw = max(5, max(len(s) for s in labels))
        if cellw % 2 == 0:
            cellw += 1  # force odd width for exact centering

        H = len(levels)
        slots_total = 1 << H
        total_width = slots_total * cellw

        # centers per level
        centers_per_level: List[List[int]] = []
        for d, level in enumerate(levels):
            span = (1 << (H - d)) * cellw
            first_center = span // 2
            centers_per_level.append([first_center + k * span for k in range(len(level))])

        # helper: color spans AFTER fixed-width placement
        def apply_blue(line: str, spans: List[tuple[int, int]]) -> str:
            if not spans:
                return line
            spans.sort()
            merged = []
            for s, e in spans:
                if not merged or s > merged[-1][1]:
                    merged.append([s, e])
                else:
                    merged[-1][1] = max(merged[-1][1], e)
            out, last = [], 0
            for s, e in merged:
                out.append(line[last:s])
                out.append(BOLD + BLUE + line[s:e] + RESET)
                last = e
            out.append(line[last:])
            return "".join(out)

        lines: List[str] = []
        half = cellw // 2

        for d, level in enumerate(levels):
            # Node row
            row = [" "] * total_width
            node_spans: List[tuple[int, int]] = []
            centers = centers_per_level[d]

            for k, idx in enumerate(level):
                c = centers[k]
                text = f"{idx}:{self.A[idx]}".center(cellw)
                start = max(0, c - half)
                end = min(total_width, start + cellw)
                row[start:end] = list(text[:end - start])
                if idx in highlights:
                    node_spans.append((start, end))

            node_line = "".join(row)  # keep trailing spaces for alignment

            # Connector row (except last level)
            if d < H - 1:
                conn = [" "] * total_width
                conn_spans: List[tuple[int, int]] = []
                child_centers = centers_per_level[d + 1]
                next_level_start = levels[d + 1][0]

                for k, idx in enumerate(level):
                    parent_c = centers[k]
                    left = 2 * idx + 1
                    right = 2 * idx + 2

                    if left < n:
                        li = left - next_level_start
                        if 0 <= li < len(child_centers):
                            lc = child_centers[li]
                            mid = (parent_c + lc) // 2
                            conn[mid] = "/"
                            if idx in highlights or left in highlights:
                                conn_spans.append((mid, mid + 1))

                    if right < n:
                        ri = right - next_level_start
                        if 0 <= ri < len(child_centers):
                            rc = child_centers[ri]
                            mid = (parent_c + rc) // 2
                            conn[mid] = "\\"
                            if idx in highlights or right in highlights:
                                conn_spans.append((mid, mid + 1))

                # apply coloring after placement
                node_line = apply_blue(node_line, node_spans)
                conn_line = apply_blue("".join(conn), conn_spans)
                lines.append(node_line)
                lines.append(conn_line)
            else:
                # last level
                lines.append(apply_blue(node_line, node_spans))

        return "\n".join(lines)




# ------------------------------- REPL Shell ----------------------------------

BANNER = r"""
Interactive Min-Heap Demo (with blue highlights)
Type 'help' to see commands. Values can be ints or any comparable types.
"""

HELP = """
Commands
--------
help                        Show this help.
viz | visualize             Print the heap as array and ASCII tree.
push X | insert X           Insert value X (e.g., push 7, push -3, push "a").
pop | extractmin            Remove and print the minimum element.
delete i | del i            Remove from the heap the element at the index i.
peek | findmin              Print the current minimum.
len                         Print number of elements.
clear                       Empty the heap.
load [a,b,c,...]            Replace heap with given list, then heapify.
heapify                     Re-heapify the current array.
random N [lo hi]            Load N random ints; optional range lo..hi (defaults 0..100).
verbose on|off              Toggle step-by-step colored tracing.
array                       Show only the underlying array.
quit | exit                 Leave the program.
"""

def parse_value(token: str):
    try:
        return ast.literal_eval(token)
    except Exception:
        return token

def parse_list(expr: str):
    v = ast.literal_eval(expr)
    if not isinstance(v, list):
        raise ValueError("not a list")
    return v

def cmd_loop():
    print(BANNER)
    h = MinHeap([])

    while True:
        try:
            line = input("minheap> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not line:
            continue

        parts = line.split()
        cmd, args = parts[0].lower(), parts[1:]

        try:
            if cmd in ("quit", "exit"):
                break
            elif cmd in ("help", "?"):
                print(HELP)
            elif cmd in ("viz", "visualize"):
                h.visualize()
            elif cmd == "array":
                print("Array:", h._format_array(set()))
            elif cmd in ("push", "insert"):
                if not args:
                    print("Usage: push X")
                    continue
                x = parse_value(" ".join(args))
                h.push(x)
                h.visualize()
            elif cmd in ("pop", "extractmin"):
                v = h.pop()
                print("popped:", v)
                h.visualize()
            elif cmd in ("peek", "findmin"):
                print("min:", h.peek())
            elif cmd == "len":
                print(len(h))
            elif cmd == "clear":
                h.clear()
                h.visualize()
            elif cmd == "load":
                if not args:
                    print("Usage: load [a,b,c,...]")
                    continue
                data = parse_list(" ".join(args))
                h.heapify_from(data)
                h.visualize("Loaded + heapified")
            elif cmd == "heapify":
                h._heapify()
                h.visualize("Heapified")
            elif cmd == "random":
                if not args:
                    print("Usage: random N [lo hi]")
                    continue
                N = int(args[0])
                lo, hi = (int(args[1]), int(args[2])) if len(args) >= 3 else (0, 100)
                data = [random.randint(lo, hi) for _ in range(N)]
                h.heapify_from(data)
                h.visualize(f"Random {N} in [{lo},{hi}] + heapified")
            elif cmd == "verbose":
                if not args or args[0].lower() not in ("on", "off"):
                    print("Usage: verbose on|off")
                    continue
                h.verbose = (args[0].lower() == "on")
                print(f"verbose = {h.verbose}")
            elif cmd in ("delete", "del"):
                if not args:
                    print("Usage: delete INDEX")
                    continue
                idx = int(args[0])
                val = h.delete_at(idx)
                print(f"deleted index {idx}: {val}")
                h.visualize()                
            else:
                print(f"Unknown command: {cmd}. Type 'help'.")
        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    cmd_loop()
