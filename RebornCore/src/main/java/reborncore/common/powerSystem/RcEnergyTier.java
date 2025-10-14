/*
 * This file is part of RebornCore, licensed under the MIT License (MIT).
 *
 * Copyright (c) 2022 TeamReborn
 *
 * Permission is hereby granted, free of charge, to any person obtaining a copy
 * of this software and associated documentation files (the "Software"), to deal
 * in the Software without restriction, including without limitation the rights
 * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 * copies of the Software, and to permit persons to whom the Software is
 * furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all
 * copies or substantial portions of the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 * SOFTWARE.
 */

package reborncore.common.powerSystem;

/**
 * Standard input / output limits for RC-based machines.
 */
public enum RcEnergyTier {
	LV(8, 8),
	MV(32, 32),
	HV(128, 128),
	EV(512, 512),
	IV(2048, 2048),
	LUV(8192, 8192),
	ZPM(32768, 32768),
	UV(131072, 131072),
	UHV(524288, 524288),
	UEV(2097152, 2097152),
	UIV(8388608, 8388608),
	UXV(33554432, 33554432),
	MAX(134217728, 134217728),
	INFINITE(Integer.MAX_VALUE, Integer.MAX_VALUE);

	private final long maxInput;
	private final long maxOutput;

	RcEnergyTier(long maxInput, long maxOutput) {
		this.maxInput = maxInput;
		this.maxOutput = maxOutput;
	}

	public long getMaxInput() {
		return maxInput;
	}

	public long getMaxOutput() {
			return maxOutput;
		}

	public static RcEnergyTier getTier(long power) {
		for (RcEnergyTier tier : RcEnergyTier.values()) {
			if (tier.getMaxInput() >= power) {
				return tier;
			}
		}
		return RcEnergyTier.INFINITE;
	}
}
